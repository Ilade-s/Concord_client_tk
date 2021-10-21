
DicoClient = {"145641231":{"pseudo":"ok","client":"fonction"}}
client="fonction"
for cle,element in DicoClient.items():
    print(element)
    if element["client"] == client:
        print("je pop "+cle)