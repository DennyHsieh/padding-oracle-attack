# Padding Oracle Attack

Decrypt the whole cipher text.

## Server
- IP: 140.122.185.174
- Port: 8081

### Initial cipher text
- Get the cipher text as below if I execute the initial client.py.
    - Try to break the system! (Decrypt it!)

```
5468697320697320616e20495634353680df47c094098bf18b0674c8efe1d97002c535a78e9829a961549254f2eab2d86286f73f839b63f2ad9ac24e8307ecab208699d3e58f8627339a4c9111c73616381bda08bb53e5dbbb86dc4f2d0418350f8100b5502ec5dc8a608e31445f0e955e123ffa80d6ae86bce208ecef64f205
```

- IV_plaintext(hex): 5468697320697320616e204956343536
- The IV is: This is an IV456

- Execute log and result

```
The whole ciphertext is:
b'5468697320697320616e20495634353680df47c094098bf18b0674c8efe1d97002c535a78e9829a961549254f2eab2d86286f73f839b63f2ad9ac24e8307ecab208699d3e58f8627339a4c9111c73616381bda08bb53e5dbbb86dc4f2d0418350f8100b5502ec5dc8a608e31445f0e955e123ffa80d6ae86bce208ecef64f205'

Directly decrypt the ciphertext, and we can see the plaintext of IV of first 16 bytes
b"This is an IV456\x80\xdfG\xc0\x94\t\x8b\xf1\x8b\x06t\xc8\xef\xe1\xd9p\x02\xc55\xa7\x8e\x98)\xa9aT\x92T\xf2\xea\xb2\xd8b\x86\xf7?\x83\x9bc\xf2\xad\x9a\xc2N\x83\x07\xec\xab \x86\x99\xd3\xe5\x8f\x86'3\x9aL\x91\x11\xc76\x168\x1b\xda\x08\xbbS\xe5\xdb\xbb\x86\xdcO-\x04\x185\x0f\x81\x00\xb5P.\xc5\xdc\x8a`\x8e1D_\x0e\x95^\x12?\xfa\x80\xd6\xae\x86\xbc\xe2\x08\xec\xefd\xf2\x05"

======
Start to try block 8
The IV(temp) encrypted text we need to change elements is:0f8100b5502ec5dc8a608e31445f0e95
The block we want to try is:5e123ffa80d6ae86bce208ecef64f205
possible padding size is: 1
possible padding size is: 8
good padding size is: 8
'e\x08\x08\x08\x08\x08\x08\x08\x08'
'2e\x08\x08\x08\x08\x08\x08\x08\x08'
'32e\x08\x08\x08\x08\x08\x08\x08\x08'
'732e\x08\x08\x08\x08\x08\x08\x08\x08'
'5732e\x08\x08\x08\x08\x08\x08\x08\x08'
'65732e\x08\x08\x08\x08\x08\x08\x08\x08'
'd65732e\x08\x08\x08\x08\x08\x08\x08\x08'
'6d65732e\x08\x08\x08\x08\x08\x08\x08\x08'
If remove padding off, the last block is:
'6d65732e'

======
Start to try block 7
The IV(temp) encrypted text we need to change elements is:381bda08bb53e5dbbb86dc4f2d041835
The block we want to try is:0f8100b5502ec5dc8a608e31445f0e95
'9'
'69'
'469'
'7469'
'07469'
'207469'
'6207469'
'66207469'
'f66207469'
'6f66207469'
'06f66207469'
'206f66207469'
'4206f66207469'
'74206f66207469'
'374206f66207469'
'7374206f66207469'

======
Start to try block 6
The IV(temp) encrypted text we need to change elements is:208699d3e58f8627339a4c9111c73616
The block we want to try is:381bda08bb53e5dbbb86dc4f2d041835
'2'
'72'
'f72'
'6f72'
'76f72'
'776f72'
'0776f72'
'20776f72'
'520776f72'
'6520776f72'
'86520776f72'
'686520776f72'
'4686520776f72'
'74686520776f72'
'074686520776f72'
'2074686520776f72'

======
Start to try block 5
The IV(temp) encrypted text we need to change elements is:6286f73f839b63f2ad9ac24e8307ecab
The block we want to try is:208699d3e58f8627339a4c9111c73616
'3'
'73'
'173'
'6173'
'76173'
'776173'
'0776173'
'20776173'
'420776173'
'7420776173'
'97420776173'
'697420776173'
'0697420776173'
'20697420776173'
'c20697420776173'
'2c20697420776173'

======
Start to try block 4
The IV(temp) encrypted text we need to change elements is:02c535a78e9829a961549254f2eab2d8
The block we want to try is:6286f73f839b63f2ad9ac24e8307ecab
'3'
'73'
'573'
'6573'
'd6573'
'6d6573'
'96d6573'
'696d6573'
'4696d6573'
'74696d6573'
'074696d6573'
'2074696d6573'
'62074696d6573'
'662074696d6573'
'f662074696d6573'
'6f662074696d6573'

======
Start to try block 3
The IV(temp) encrypted text we need to change elements is:80df47c094098bf18b0674c8efe1d970
The block we want to try is:02c535a78e9829a961549254f2eab2d8
'0'
'20'
'420'
'7420'
'37420'
'737420'
'5737420'
'65737420'
'265737420'
'6265737420'
'06265737420'
'206265737420'
'5206265737420'
'65206265737420'
'865206265737420'
'6865206265737420'

======
Start to try block 2
The IV(temp) encrypted text we need to change elements is:5468697320697320616e204956343536
The block we want to try is:80df47c094098bf18b0674c8efe1d970
'4'
'74'
'074'
'2074'
'32074'
'732074'
'1732074'
'61732074'
'761732074'
'7761732074'
'07761732074'
'207761732074'
'4207761732074'
'74207761732074'
'974207761732074'
'4974207761732074'
The plaintext_hex is: 497420776173207468652062657374206f662074696d65732c206974207761732074686520776f727374206f662074696d65732e
The IV is: This is an IV456
The plaintext is: It was the best of times, it was the worst of times.
```

