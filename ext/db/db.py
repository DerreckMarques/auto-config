#executar esse script na linha de comando para inicializar o banco de dados
import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO hosts (hostname, ip) VALUES (?, ?)",
            ('IFTO-Gurupi', '200.139.25.33')
            )

cur.execute("INSERT INTO scripts (title, content) VALUES (?, ?)",
            ('Boas Práticas', 
            '''set system services ssh root-login deny \n
            set routing-options static defaults passive <br>
            set interfaces ge-0/0/0 unit 0 family inet rpf-check
            set interfaces irb unit 1554 family inet rpf-check
            
            set system services ssh no-tcp-forwarding
            set system services ssh connection-limit
            set system services ssh rate-limit
            
            
            set system internet-options path-mtu-discovery
            set system internet-options gre-path-mtu-discovery
            set system internet-options no-source-quench
            set system internet-options tcp-drop-synfin-set 
            set system internet-options ipv6-path-mtu-discovery 
            set system internet-options no-tcp-reset drop-tcp-with-syn-only
            
            set system no-redirects
            set system no-redirects-ipv6''')
            )

hosts = cur.execute('SELECT * FROM hosts').fetchall()

print(hosts)


connection.commit()
connection.close()