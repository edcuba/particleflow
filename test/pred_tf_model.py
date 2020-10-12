import os
import time
import glob
import numpy as np

def get_X(X,y,w):
    return X

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="PFNet", help="type of model to train", choices=["PFNet"])
    parser.add_argument("--weights", type=str, default=None, help="model weights to load")
    parser.add_argument("--nhidden", type=int, default=256, help="hidden dimension")
    parser.add_argument("--distance-dim", type=int, default=256, help="distance dimension")
    parser.add_argument("--num-conv", type=int, default=1, help="number of convolution layers")
    parser.add_argument("--nthreads", type=int, default=-1, help="number of threads to use")
    parser.add_argument("--ntrain", type=int, default=80, help="number of training events")
    parser.add_argument("--ntest", type=int, default=20, help="number of testing events")
    parser.add_argument("--gpu", action="store_true", help="use GPU")
    parser.add_argument("--convlayer", type=str, default="sgconv", choices=["sgconv", "ghconv"], help="Type of graph convolutional layer")
    parser.add_argument("--datapath", type=str, help="Input data path", required=True)
    parser.add_argument("--target", type=str, choices=["cand", "gen"], help="Regress to PFCandidates or GenParticles", default="gen")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()

    if args.gpu:
        import setGPU
    else:
        os.environ["CUDA_VISIBLE_DEVICES"] = ""

    import tensorflow as tf

    physical_devices = tf.config.list_physical_devices('GPU')
    if len(physical_devices) > 0:
        tf.config.experimental.set_memory_growth(physical_devices[0], True)
    tf.config.experimental_run_functions_eagerly(False)

    from tf_model import batch_size, num_max_elems

    tf.gfile = tf.io.gfile
    from tf_model import PFNet, prepare_df
    from tf_data import _parse_tfr_element
    tfr_files = glob.glob("{}/tfr/{}/*.tfrecords".format(args.datapath, args.target))
    assert(len(tfr_files)>0)
    #tf.config.optimizer.set_jit(True)

    if args.nthreads > 0:
        tf.config.threading.set_inter_op_parallelism_threads(args.nthreads)
        tf.config.threading.set_intra_op_parallelism_threads(args.nthreads)
    if not args.gpu:
        tf.config.set_visible_devices([], 'GPU')

    nev = args.ntest
    ps = (tf.TensorShape([num_max_elems, 15]), tf.TensorShape([num_max_elems, 5]), tf.TensorShape([num_max_elems, ]))
    dataset = tf.data.TFRecordDataset(tfr_files).map(
        _parse_tfr_element, num_parallel_calls=tf.data.experimental.AUTOTUNE).skip(args.ntrain).take(nev).padded_batch(batch_size, padded_shapes=ps)
    dataset_X = dataset.map(get_X)

    model = PFNet(hidden_dim=args.nhidden, distance_dim=args.distance_dim, num_conv=args.num_conv, convlayer=args.convlayer)
    model = model.create_model()

    #ensure model is compiled
    neval = 0
    for X in dataset_X:
        print(X.shape)
        model(X)
        neval += 1
        break
    assert(neval > 0)

    #load the weights
    model.load_weights(args.weights)

    #prepare the dataframe
    prepare_df(0, model, dataset, ".", "cand", save_raw=False)

    print("now timing")
    t0 = time.time()
    for X in dataset_X:
        model.predict_on_batch(X)
    print()
    t1 = time.time()
    time_per_dsrow = (t1-t0)/len(dataset_X)
    print("prediction time per event: {:.2f} ms".format(1000.0*(t1-t0)/(nev/batch_size)))

    #https://leimao.github.io/blog/Save-Load-Inference-From-TF2-Frozen-Graph/
    

    # Get frozen ConcreteFunction
    full_model = tf.function(lambda x: model(x))
    full_model = full_model.get_concrete_function(
        tf.TensorSpec((batch_size, num_max_elems, 15), tf.float32))
    from tensorflow.python.framework import convert_to_constants
    frozen_func = convert_to_constants.convert_variables_to_constants_v2(full_model)
    frozen_func.graph.as_graph_def()
    print(full_model.graph.inputs)
    print(full_model.graph.outputs)

    tf.io.write_graph(graph_or_graph_def=frozen_func.graph,
                      logdir="./model_frozen",
                      name="frozen_graph.pb",
                      as_text=False)

    #model.save('model', overwrite=True, include_optimizer=False)
