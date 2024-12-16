from lxml import etree

INXML = 'interim_output/TR_EN_prod.html'
#INXML = 'interim_output/dict_test_v2.html'

WORD = 'ağzına'
#WORD='denizine'

parser = etree.XMLParser(ns_clean=True)
root = etree.parse(INXML, parser)

#print(root.xpath("//*local-name()='orth'[@value='denizine']"))
orths = root.xpath("//idx:orth[@value='"+WORD+"']", namespaces={'idx':"www.mobipocket.com/idx"})
iforms = root.xpath("//idx:iform[@value='"+WORD+"']", namespaces={'idx':"www.mobipocket.com/idx"})

print(f"Looking for :: {WORD} in file :: {INXML}")
print(f"orths : {[e.attrib['value'] for e in orths]}")
print(f"iforms: {[e.attrib['value'] for e in iforms]}")
