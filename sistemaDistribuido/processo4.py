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

	
	def receber(self):
		while True:
			try:
				msg, cliente = self.my_socket.recvfrom(1024)
			except:
				print("Aguardando...")
	
	def eleicao(self):

		msg = input()

		if msg == "":

			if self.lider != True:

				print("Iniciando uma eleicao...")

				# prepara pacote eleicao
				pe = self.empacotar("valetao",self.id)

				self.my_socket.sendto(pe.encode(),(IP_BROADCAST,PORTA))

				while True:
					try:
						msg, cliente = self.my_socket.recvfrom(1024)
						
						if clinte[0] != self.host:

							po = desempacotar(msg)
							
							if po[0] == "ok":

								self.lider = False
					except:
						print("Tempo esgotado")
						print("Sou o lider")
						self.lider = True
						print("Iniciando berkley")

						

			elif self.lider == True:


class Relogio():

	def __init__(self):
		self.incr = 6
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