# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 21:57:12 2019

@author: sibel
"""
import textwrap
import tkinter as tk
import tkinter.ttk as ttk
import random
#%%
def generate_humming(string_bits):
    list_=textwrap.wrap(string_bits,4)
    coded_list=[]
    for a in list_:
        b=a [::-1]
        r0=str((int(b[0])+int(b[1])+int(b[2]))%2)
        r1=str((int(b[3])+int(b[2])+int(b[1]))%2)
        r2=str((int(b[1])+int(b[0])+int(b[3]))%2)
        a=str(a)+r2+r1+r0
        coded_list.append(a)
    return coded_list
    
#%%    
def make_error(coded_list):
     corrupted_bits=[]
     for a in coded_list:
         a=list(a)
         err_position=random.randint(0,3)
         if(a[err_position]=="0"):
             a[err_position]="1"
         else:
             a[err_position]="0"
         corrupted_bits.append("".join(a))   
     return corrupted_bits
    
    
#%%
     
def err_positions(corrupted_bits):
        err_positions=[]
        for a in corrupted_bits:
             
             s0=str((int(a[1])+int(a[2])+int(a[3])+int(a[6]))%2)
             s1=str((int(a[0])+int(a[1])+int(a[2])+int(a[5]))%2)
             s2=str((int(a[2])+int(a[3])+int(a[0])+int(a[4]))%2)
            
             if((s2+s1+s0)=="001"):
                  err_positions.append(6)
             elif((s2+s1+s0)=="010"):
                  err_positions.append(5)
             elif((s2+s1+s0)=="011"):
                  err_positions.append(1)
             elif((s2+s1+s0)=="100"):
                  err_positions.append(4)
             elif((s2+s1+s0)=="101"):
                  err_positions.append(3)
             elif((s2+s1+s0)=="110"):
                  err_positions.append(0)
             elif((s2+s1+s0)=="111"):
                  err_positions.append(2)
             else:
                print("no error!")
       
        return err_positions
#%%
        
    
def fix_errors(corrupted_bits,err_positions):
    fixed_bits=[]
    
    for i,v in enumerate(corrupted_bits):
        list_err=list(corrupted_bits[i])
        list_err[err_positions[i]]=toggle(list_err[err_positions[i]])
        fixed_bits.append("".join(list_err[:4]))
    
    return fixed_bits
#%%
    
def toggle(s):
    if(s=="0"):
        s="1"
    else:
        s="0"
    return s
    
#%%
def binary_converter(string):
    for character in string:
        return str(bin(ord(character))[2:].zfill(8))

def decode_binary_string(s):
    
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))


#%%
def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def get_corrupted_text(s):
    binaries=[]
    for i,e in enumerate(s):
        a=s[i][:4]
        binaries.append(a)
    a=text_from_bits("".join(binaries))
    return  a


#%%
root = tk.Tk()
root.title("Hamming Code App")
 
root.geometry('600x300')

#%%
def clicked():

        text= len(entry.get())
        if(text!=0):
            raw_text=entry.get()
            ascii_bits=""
            for index, char in enumerate(raw_text):
                ascii_bits=ascii_bits + binary_converter(char)
            lbl_bit_return.configure(text=ascii_bits)
            
            return_=generate_humming(ascii_bits)
            lbl_kod_return.configure(text=return_)
            corrupted_bit=make_error(return_)
            err_pos=err_positions(corrupted_bit)
            lbl_err_return.configure(text=corrupted_bit)
            lbl_err_bit_return.configure(text=err_pos)
            fixed=fix_errors(corrupted_bit,err_pos)
            lbl_trusted_return.configure(text="".join(fixed))
            lbl_err_text_return.configure(text=get_corrupted_text(corrupted_bit))
            lbl_real_return.configure(text=decode_binary_string("".join(fixed)))
        else:
             from tkinter import messagebox
             messagebox.showinfo("UYARI", "Bir metin giriniz!")
             
lbl_duz = tk.Label(root, text="İletilecek Metin:",font=("Helvetica", 12),justify=tk.LEFT)
lbl_duz.grid(column=0,sticky = tk.W, row=0)
entry = tk.Entry(root,width=50)
entry.grid(column=1,row=0)

#%%

lbl_bit = tk.Label(root, text="İletilecek Doğru Bitler:",font=("Helvetica", 12),justify=tk.LEFT)
lbl_bit.grid(column=0,sticky = tk.W, row=1)

lbl_bit_return=tk.Label(root, text="",font=("Helvetica", 12),justify=tk.LEFT)
lbl_bit_return.grid(column=1,sticky = tk.W, row=1)


#%%
lbl_kod = tk.Label(root, text="İletilecek Kodlanmış Bitler:",font=("Helvetica", 12),justify=tk.LEFT)
lbl_kod.grid(column=0,sticky = tk.W, row=2)

lbl_kod_return=tk.Label(root, text="",font=("Helvetica", 12),justify=tk.LEFT)
lbl_kod_return.grid(column=1,sticky = tk.W, row=2)



#%%
lbl_err = tk.Label(root, text="Hata Eklenmiş Bitler:",font=("Helvetica", 12),justify=tk.LEFT)
lbl_err.grid(column=0,sticky = tk.W, row=3)

lbl_err_return=tk.Label(root, text="",font=("Helvetica", 12),justify=tk.LEFT)
lbl_err_return.grid(column=1,sticky = tk.W, row=3)


#%%
lbl_err_bit = tk.Label(root, text="Hatalı Bitler:",font=("Helvetica", 12),fg="red",justify=tk.LEFT)
lbl_err_bit.grid(column=0, sticky = tk.W,row=4)

lbl_err_bit_return=tk.Label(root, text="",font=("Helvetica", 12),fg="red",justify=tk.LEFT)
lbl_err_bit_return.grid(column=1,sticky = tk.W, row=4)

#%%
lbl_err_text = tk.Label(root, text="Hatalı Metin:",font=("Helvetica", 12),fg="red",justify=tk.LEFT)
lbl_err_text.grid(column=0, sticky = tk.W,row=5)

lbl_err_text_return=tk.Label(root, text="",font=("Helvetica", 12),fg="red",justify=tk.LEFT)
lbl_err_text_return.grid(column=1,sticky = tk.W, row=5)
#%%

lbl_trusted= tk.Label(root, text="Düzeltilmiş Bitler:",font=("Helvetica", 12), anchor=tk.W,justify=tk.LEFT)
lbl_trusted.grid(column=0,sticky = tk.W, row=6)

lbl_trusted_return=tk.Label(root, text="",font=("Helvetica", 12),justify=tk.LEFT)
lbl_trusted_return.grid(column=1,sticky = tk.W, row=6)


#%%

lbl_real= tk.Label(root, text="Asıl Metin:",font=("Helvetica", 12), anchor=tk.W,justify=tk.LEFT)
lbl_real.grid(column=0,sticky = tk.W, row=7)

lbl_real_return=tk.Label(root, text="",font=("Helvetica", 12),justify=tk.LEFT)
lbl_real_return.grid(column=1,sticky = tk.W, row=7)
#%%
btn = tk.Button(root, text="SEND", bg="black", fg="white", command=clicked)
btn.grid(column=2, row=0)


root.mainloop()