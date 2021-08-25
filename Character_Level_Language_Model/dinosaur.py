import warnings
warnings.filterwarnings('ignore')
from colorama import Fore
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU,Embedding,Dense
from tensorflow.keras.losses import sparse_categorical_crossentropy

def generate_text(model,char_to_idx ,idx_to_char, start_seed,gen_size=100,temp=1.0):

    num_generate = gen_size

    input_eval = [char_to_idx[s] for s in start_seed]

    input_eval = tf.expand_dims(input_eval, 0)

    text_generated = []

    temperature = temp
    model.reset_states()

    for i in range(num_generate):

        predictions = model(input_eval)

        predictions = tf.squeeze(predictions, 0)

        predictions = predictions / temperature
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()
        
        input_eval = tf.expand_dims([predicted_id], 0)

        text_generated.append(idx_to_char[predicted_id])

    return (start_seed + ''.join(text_generated))


def generate(ctoi,itoc):
    print(Fore.CYAN)
    start_seed = input("Enter the start string:  ")
    nc = int(input("Enter the number of characters: "))
    temp = float(input("Enter the entropy (float): "))
    new_string = generate_text(models,ctoi,itoc,start_seed,nc,temp)
    print("\n")
    print("We have a new dinosaur discovered!!! It is ......")
    print(Fore.RED,new_string)
    print(Fore.WHITE,"\n")
    response = input("Do you like it (y/n): ")
    if response == 'n':
        generate(ctoi,itoc)
    else:
        print(Fore.CYAN,"Thanks")

def sparse_cat_loss(y_true,y_pred):
    return sparse_categorical_crossentropy(y_true,y_pred,from_logits=True)

def create_model(vocab_size, embed_dim, rnn_neurons, batch_size):
    model = Sequential()
    model.add(Embedding(vocab_size, embed_dim,batch_input_shape=[batch_size, None]))
    model.add(GRU(rnn_neurons,return_sequences=True,stateful=True,recurrent_initializer='glorot_uniform'))
    # Final Dense Layer to Predict
    model.add(Dense(vocab_size))
    model.compile(optimizer='adam', loss=sparse_cat_loss) 
    return model

if __name__ == '__main__':
    with open('./dinos.txt','r') as dino:
        dinos = dino.read()

    dinos = dinos.lower()
    new = []
    char  = ""
    for ch in dinos:
        if ch != '\n':
            char = char + ch
        else:
            new.append(len(char))
            char = ""

    char = list(set(dinos))
    char_to_idx = {c:i for i,c in enumerate(sorted(char))}
    idx_to_char = {i:c for i,c in enumerate(sorted(char))}  
    embed_dim = 32
    vocab_size = len(char)
    rnn_neurons = 1024
    
    models = create_model(vocab_size,embed_dim,rnn_neurons,batch_size=1)
    models.load_weights('./dino.h5')
    models.build(tf.TensorShape([1, None]))

    generate(char_to_idx,idx_to_char)