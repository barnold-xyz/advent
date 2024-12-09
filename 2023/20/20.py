data = open("2023/20/test2.txt").read().split('\n')

type_sym_to_str = {'b': 'broadcast', '%': 'flipflop', '&': 'conj'}

modules = {}
modules['button'] = {'type': 'broadcast', 'dest': ['roadcaster']}
for line in data: 
    name, *dest = line.replace(' -> ',' ').replace(',', '').split(' ')
    mod_type = type_sym_to_str[name[0]]
    name = name[1:]
    if len(dest) == 1:
        dest = [dest[0]]
    modules[name] = {'type': mod_type, 'dest': dest}

# add sources to conj modules
for conj_name, conj_mod in modules.items():
    if conj_mod['type'] == 'conj':
        conj_mod['sources'] = {name: 'lo' for name, mod in modules.items() if conj_name in mod['dest']}

# initialize flipflop modules
for name, mod in modules.items():
    if mod['type'] == 'flipflop':
        mod['state'] = 'off'

# deal with output module if needed
addl_modules = {}
for name, mod in modules.items():
    for dest in mod['dest']:
        if dest not in modules:
            addl_modules[dest] = {'type': 'broadcast', 'dest': []}
modules.update(addl_modules)

def process_pulse(pulse, pending_pulses):
    input_pulse_type, source, dest = pulse
    print(f'pulse: {pulse}')
    send_pulse = False
    output_pulse_type = None
    global pulse_count
    if modules[dest]['type'] == 'broadcast':
        send_pulse = True
        output_pulse_type = input_pulse_type
    elif modules[dest]['type'] == 'flipflop':
        if input_pulse_type == 'lo':
            output_pulse_type = 'hi' if modules[dest]['state'] == 'off' else 'lo'
            modules[dest]['state'] = 'on' if modules[dest]['state'] == 'off' else 'on'
            send_pulse = True
    elif modules[dest]['type'] == 'conj':
        modules[dest]['sources'][source] = input_pulse_type
        #print(modules[dest])
        #print('in conj, sources: ',modules[dest]['sources'].values())
        if all(value == 'lo' for value in modules[dest]['sources'].values()):
            #print('all hi')
            output_pulse_type = 'hi'
            send_pulse = True
        elif all(value == 'hi' for value in modules[dest]['sources'].values()):
            #print('all lo')
            output_pulse_type = 'lo'
            send_pulse = True
        #else: 
            #print(dest, 'not all hi or lo: ', modules[dest]['sources'].values())
        print(f'  conj: {dest} {modules[dest]['sources'].values()} {send_pulse} {output_pulse_type} {modules[dest]['dest']}')
    else:
        raise ValueError('Invalid module type: ' + modules[dest]['type'])
    if send_pulse:
        for d in modules[dest]['dest']:
            pending_pulses.append((output_pulse_type, dest, d))

#print(modules['inv']); quit()
#print(data)
#for item in modules.items():
#    print(item)
#quit()

pulse_count = 0

def push_button():
    global pulse_count
    pending_pulses = [('lo', 'button', 'roadcaster')]
    while pending_pulses:
        pulse = pending_pulses.pop(0)
        pulse_count += 1
        process_pulse(pulse, pending_pulses)
    print(pulse_count)

push_button()
push_button()
push_button()
push_button()
