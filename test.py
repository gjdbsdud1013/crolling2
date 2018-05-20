from firebase import firebase

firebase = firebase.FirebaseApplication('https://chat-9892b.firebaseio.com/')

result = firebase.post('/',{'news{0}'.format(i):'11111'})
print(result)