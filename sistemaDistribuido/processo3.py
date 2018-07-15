import socket,threading,time,sys

IP_BROADCAST = "255.255.255.255"
PORTA		 = 5000

class Processo():

	def __init__(self,idProcesso):

		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.my_socket.settimeout(10)
		self.my_socket.bind(('', PORTA))
		
		self.id = idProcesso
		self.host = '192.168.1.10' 
		#self.peer = self.my_socket.getpeername()
		self.lider = False
		self.relogio = Relogio()
		self.soma = 0
		self.processos = []

		threading.Thread(target=self.relogio.incrRelogio).start()
		threading.Thread(target=self.receber).start()
		threading.Thread(target=self.eleicao).start()
		print("Id de processo eh: ",self.id)
		
		self.relogio.mostrarHora()

	def empacotar(self,msg,valor):
		return msg+":"+str(valor)

	def desempacotar(self,pacote):
		return pacote.decode("utf-8").split(":")

	
	def enviar(self):
		while True:
			msg = input()
			self.my_socket.sendto(msg.encode(),(IP_BROADCAST,PORTA))
	 	

	def unicast(self,msg):
		print("unicast")
		print("tamanho processos:",self.processos)
		if len(self.processos) > 0:
			for p in self.processos:
				print("Enviando para:",p)
				self.my_socket.sendto(msg.encode(),p)
	
	def receber(self):
		while True:
			try:
				msg, cliente = self.my_socket.recvfrom(1024)

				if cliente[0] != self.host: 
					p = self.desempacotar(msg)

					if p[0] == "lider" or p[0] == "ok":
						print("Nao sou lider")
						self.lider = False
					
					elif p[0] == "valentao":

						if int(p[1]) < self.id:
							po = self.empacotar("ok",self.id)

							# meu id eh mando ok para quem me enviou
							self.my_socket.sendto(po.encode(),(cliente,PORTA)) 

							#convoca outra eleicao
							pv = self.empacotar("valentao",self.id)
							self.my_socket.sendto(pv.encode(),(IP_BROADCAST,PORTA)) 
						else:
							print("Sai da disputa de lideranca")
							self.lider = False

					elif p[0] == "berkeley":

						valor = int(p[1])
						defasagem = self.relogio.hora - valor
						de = self.empacotar("defasagem",defasagem) 
						self.my_socket.sendto(de.encode(),(IP_BROADCAST,PORTA))

					elif p[0] == "ajuste":
						print("ajuste ko")
						valor = int(p[1])
						novaHora = valor - self.relogio.hora
						self.relogio.hora += novaHora
						self.relogio.mostrarHora()

			except:
				print("Aguardando...")
	
	def eleicao(self):

		while True:
			
			msg = input()

			if msg == "":

				if self.lider != True: 	
							
					pv = self.empacotar("valentao",self.id)
						
					# envia msg em broadcast para comecar uma eleicao
					self.my_socket.sendto(pv.encode(),(IP_BROADCAST,PORTA))

					print("Eleicao iniciada")
				
					while True:
						try:
							msg, cliente = self.my_socket.recvfrom(1024)
							if cliente[0] != self.host:
								print("Tem processo com id maior")
						except:
							print("Tempo esgotado")
							print("Eu sou o LIDER")
							self.lider = True
							pv = self.empacotar("lider",self.id)
							self.my_socket.sendto(pv.encode(),(IP_BROADCAST,PORTA))
							break


				if self.lider == True:

					print("Executanto Berkeley")
					pb = self.empacotar("berkeley",self.relogio.hora)

					self.my_socket.sendto(pb.encode(),(IP_BROADCAST,PORTA))

					while True:
						try:
							msg, cliente = self.my_socket.recvfrom(1024)

							if cliente[0] != self.host:

								msg = self.desempacotar(msg)

								if msg[0] == "defasagem":
									print("recebi defasagem")
									d = int(msg[1])
									self.soma = self.soma + d

									self.processos.append(cliente)
									
						except:
							print("Tempo esgotado")
							print("Preparando mensagem de ajuste...")

							meuAjuste = self.soma//(len(self.processos)+1)
							print("Atualizando relogio lider...")
							self.relogio.ajustarHora(meuAjuste)

							pv = self.empacotar("ajuste",self.relogio.hora)
							self.unicast(pv)
							self.soma = 0
							break	

class Relogio():

	def __init__(self):
		self.incr = 1
		self.hora = 0

	def incrRelogio(self):

	    while True:
	    	self.hora += self.incr
	    	time.sleep(5)

	def mostrarHora(self):
		print("Minha hora eh: ",self.hora,"Valor de incr: ",self.incr)

	def ajustarHora(self,media):
		self.hora += media
		print("Hora ajustada eh:",self.hora)

	def calcularDefasagem(self, horaLider):
		pass

def main(identificador):

	p = Processo(int(identificador))

if __name__ == '__main__':
	main(sys.argv[1])