from flask import Flask,render_template,session,url_for,redirect
from flask_wtf import FlaskForm
from wtforms import TextField,SubmitField
import numpy as np
from tensorflow.keras.losses import sparse_categorical_crossentropy
from tensorflow.keras.models import Sequential
from keras.layers import GRU,Embedding,Dense
import tensorflow as tf

class Dinosaur:
    def sparse_cat_loss(self,y_true,y_pred):
        return sparse_categorical_crossentropy(y_true,y_pred,from_logits=True)

    def model_parameters(self):
        self.character =['s','y','n','t','v','q', 'f','j', 'd', 'a', 'k', 'l', 'z', 'g', 'r', 'w', 'h', 'e', 'b', 'i', 'm', 'p', '\n','u', 'o', 'c','x']
        self.char_to_idx = {c:i for i,c in enumerate(sorted(self.character))}
        self.idx_to_char = {i:c for i,c in enumerate(sorted(self.character))}
        
    def create_model(self):
        rnn_neurons = 1024
        vocab_size = len(self.character)
        embed_dim = 32
        batch_size = 64
        ## Model 
        model = Sequential()
        model.add(Embedding(vocab_size, embed_dim,batch_input_shape=[batch_size, None]))
        model.add(GRU(rnn_neurons,return_sequences=True,stateful=True,recurrent_initializer='glorot_uniform'))
        model.add(Dense(vocab_size))
        model.compile(optimizer='adam', loss=self.sparse_cat_loss) 

        return model

    def generate_text(self,model,content):   
        start_seed = content['start']
        temperature = float(content['entropy']) 
        size = int(content['size'])

        input_eval = [self.char_to_idx[s] for s in start_seed]
        input_eval = tf.expand_dims(input_eval, 0)
        text_generated = []
        model.reset_states()

        for i in range(size):
            predictions = model(input_eval)
            predictions = tf.squeeze(predictions, 0)
            predictions = predictions / temperature
            predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()
            input_eval = tf.expand_dims([predicted_id], 0)
            text_generated.append(self.idx_to_char[predicted_id])

        return (start_seed + ''.join(text_generated))

obj = Dinosaur()
obj.model_parameters()
model = obj.create_model()
model.build(tf.TensorShape([1, None]))
model.load_weights('.\dino.h5')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
class CounterForm(FlaskForm):
    start =   TextField('Start')
    entropy = TextField('Entropy')
    size =    TextField('Size')
    submit = SubmitField('Generate')

@app.route("/",methods = ["GET", "POST"])
def index():
    form = CounterForm()
    if form.validate_on_submit():
        session['start'] = form.start.data
        session['size'] = form.size.data
        session['entropy'] = form.entropy.data
        return redirect(url_for("prediction"))
    return render_template('home.html',form=form)

@app.route('/prediction')
def prediction():
    content = {}
    content['start'] = session['start']
    content['entropy'] = session['entropy']
    content['size']    =  session['size']

    results = obj.generate_text(model,content)

    return render_template('prediction.html',results=results)

if __name__ == '__main__':
    app.run()
