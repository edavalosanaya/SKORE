import mido

#mido.set_backend('mido.backends.pygame')
a = mido.get_input_names()
print(a)

"""
inport = mido.open_input(a[0])

for msg in inport:
    print(msg)
"""
