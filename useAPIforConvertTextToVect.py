from flask import Flask, jsonify, request, session
import os
app = Flask(__name__)


app.sessionVariable=0

# API to encode a list of strings to USE vector of 512 dimensions
@app.route('/encoder',  methods=['POST'])
def encoder():
    # Function so that one session can be called multiple times.
    # Useful while multiple calls need to be done for embedding.
    import tensorflow as tf
    import tensorflow_hub as hub
    import numpy as np
    sentToEncode=request.args.getlist('sentToEncode')

    def embed_useT(module):
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True

        with tf.Graph().as_default():
            sentences = tf.placeholder(tf.string)
            #export TFHUB_CACHE_DIR=/my_module_cache
            embed = hub.Module(module)
            embeddings = embed(sentences)
            session = tf.train.MonitoredSession()
        app.sessionVariable+=1
        return lambda x: session.run(embeddings, {sentences: x})

    #It takes similarity matrix (generated from sentence encoder) as input and gives index of redundant statements
    def redundant_sent_idx(sim_matrix, threshold=0.8):
        dup_idx = []
        for i in range(sim_matrix.shape[0]):
            if i not in dup_idx:
                tmp = [t+i+1 for t in list(np.where(sim_matrix[i][i+1:] > threshold)[0])]
                dup_idx.extend(tmp)
        return dup_idx

    #######
    # dup_indexes = redundant_sent_idx(sim_matrix=np.inner(encoding_matrix, encoding_matrix), threshold=0.5)
    # unique_messages = np.delete(np.array(messages), dup_indexes)
    #######

    if app.sessionVariable==0:
        app.embed_fn = embed_useT("downloadedModel/useModel/")
    embed_message = app.embed_fn(sentToEncode)
    return jsonify(embed_message.tolist())

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5456, debug=True)
