from iroha import IrohaCrypto

node1_private_key = IrohaCrypto.private_key()
node1_public_key = IrohaCrypto.derive_public_key(node1_private_key)

print('node 1 private key: ', node1_private_key)
print('node 1 public key: ', node1_public_key)



# node2_private_key = IrohaCrypto.private_key()
# node2_public_key = IrohaCrypto.derive_public_key(node2_private_key)