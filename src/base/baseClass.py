class Personagem:
    def __init__(self, name, life, level, atackDmg):
        self.__name = name    
        self.__life = life
        self.__level = level
        self.__atackDmg = atackDmg
        self.__inventario = Inventario()
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, novo):
        self.__name = novo
    
    @property
    def life(self):
        return self.__life
    
    @life.setter
    def life(self, novo):
        if novo >= 0:
            self.__life = novo
    
    @property
    def level(self):
        return self.__level
    
    @level.setter
    def level(self, novo):
        if novo > 0:
            self.__level = novo
    
    @property
    def atackDmg(self):
        return self.__atackDmg
    
    @atackDmg.setter
    def atackDmg(self, novo):
        if novo >= 0:
            self.__atackDmg = novo
    
    @property
    def inventario(self):
        return self.__inventario
    
    def atacar(self, alvo):
        if self.estaVivo():
            alvo.receberDano(self.atackDmg)
            print(f"{self.atackDmg} de dano causado")
        else:
            print("Individuo morto! Nao ataque caadaveres! Seu covarde")
    
    def receberDano(self, dmg):
        self.__life -= dmg
        if self.__life <= 0:
            print(f"{self.__name} morreu")
            self.__life = 0
    
    def estaVivo(self):
        return self.__life > 0
    
    def usarItem(self, item):
        if isinstance(item, Item):
            item.usar(self)
        else:
            print("item inexistente ou invalido")

class Player(Personagem):
    def __init__(self, name, life, level, atackDmg):
        super().__init__(name, life, level, atackDmg)
        self.__experiencia = 0
        self.__missoes = []  # para acumular missoes, sem limite para dar menos trampo
    
    @property
    def experiencia(self):
        return self.__experiencia
    
    @experiencia.setter
    def experiencia(self, novo):
        if novo >= 0:
            self.__experiencia = novo
            self.__verificarLevelUp()
    
    @property
    def missoes(self):
        return self.__missoes
    
    def aceitarMissao(self, quest):
        if isinstance(quest, Quest):
            self.__missoes.append(quest)
            quest.status = "Em andamento"
            print(f"Missão '{quest.titulo}' aceitada")
        else:
            print("Missão inválida!")
    
    def __verificarLevelUp(self):
        expNecessario = self._Personagem__level * 100
        while self.__experiencia >= expNecessario:
            self.__experiencia -= expNecessario
            self.level += 1
            self.life += 50
            self.atackDmg += 10
            print(f"{self.name} subiu de nive! novo nivel {self.level}")
            expNecessario = self._Personagem__level * 100
    
    def ganharExp(self, expGanho):
        self.__experiencia += expGanho
        print(f"Ganhou: {expGanho} de experiencia.")
        self.__verificarLevelUp()
    
    def completarMissao(self, titulo):
        for quest in self.__missoes:
            if quest.titulo == titulo and quest.status == "Em andamento":
                quest.concluir()
                self.ganharExp(quest.recompensaExp)

class Enemy(Personagem):
    def __init__(self, name, life, level, atackDmg, raca, itemDrop):
        super().__init__(name, life, level, atackDmg)
        self.__raca = raca
        self.__itemDrop = itemDrop
    
    @property
    def raca(self):
        return self.__raca
    
    @raca.setter
    def raca(self, novo):
        self.__raca = novo
    
    @property
    def itemDrop(self):
        return self.__itemDrop
    
    @itemDrop.setter
    def itemDrop(self, novo):
        self.__itemDrop = novo
    
    def dropItem(self):
        if self.__itemDrop and not self.estaVivo():
            print(f"{self.name} dropou {self.__itemDrop.name}!")
            return self.__itemDrop

class Item:
    def __init__(self, name, descricao):
        self.__name = name
        self.__descricao = descricao
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, novo):
        self.__name = novo
    
    @property
    def descricao(self):
        return self.__descricao
    
    @descricao.setter
    def descricao(self, novo):
        self.__descricao = novo
    
    def usar(self, alvo):
        print(f"usando {self.__name} em {alvo.name}")

class Quest:
    def __init__(self, titulo, descricao, recompensaExp=100):  # deixar valor padrao aqui pra facilitar dps
        self.__titulo = titulo
        self.__descricao = descricao
        self.__status = "disponivel"
        self.__recompensaExp = recompensaExp
    
    @property
    def titulo(self):
        return self.__titulo
    
    @titulo.setter
    def titulo(self, novo):
        self.__titulo = novo
    
    @property
    def descricao(self):
        return self.__descricao
    
    @descricao.setter
    def descricao(self, novo):
        self.__descricao = novo
    
    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, novo):
        # proibe atribuir outras coisas alem dessas
        if novo in ["disponivel", "Em andamento", "Concluida"]:
            self.__status = novo
    
    @property
    def recompensaExp(self):
        return self.__recompensaExp
    
    @recompensaExp.setter
    def recompensaExp(self, novo):
        if novo >= 0:
            self.__recompensaExp = novo
    
    def concluir(self):
        self.__status = "Concluida"
    
    @property
    def concluida(self):
        return self.__status == "Concluida"

class Inventario:
    def __init__(self):
        self.__itens = []
    
    def addItem(self, item):
        if isinstance(item, Item):
            self.__itens.append(item)
            print(f" {item.name} adicionado ao inventario")
        else:
            print("Item nao existe")
    
    def removerItem(self, item):
        if item in self.__itens:
            self.__itens.remove(item)
            print(f" {item.name} removido do inventario")
            return True
        else:
            print(f"{item.name} nao encontrado no seu inventario")
            return False
    
    def listarItens(self):
        if not self.__itens:
            print("inventario vazio")
            return []
        for i, item in enumerate(self.__itens, 1):
            print(f"{item.name} |-| {item.descricao}")
        return self.__itens
    
    @property
    def itens(self):
        return self.__itens.copy()

class Arma(Item):
    def __init__(self, name, descricao, dano):
        super().__init__(name, descricao)
        self.__dano = dano
    
    @property
    def dano(self):
        return self.__dano
    
    @dano.setter
    def dano(self, novo):
        if novo >= 0:
            self.__dano = novo
    
    def usar(self, alvo):
        if isinstance(alvo, Personagem):
            alvo.atackDmg += self.__dano
            print(f"{alvo.name} agora tem {alvo.atackDmg} de dano por ter equipado {self.name}")
        else:
            super().usar(alvo)

class Armadura(Item):
    def __init__(self, name, descricao, defesa):
        super().__init__(name, descricao)
        self.__defesa = defesa
    
    @property
    def defesa(self):
        return self.__defesa
    
    @defesa.setter
    def defesa(self, novo):
        if novo >= 0:
            self.__defesa = novo
    
    def usar(self, alvo):
        if isinstance(alvo, Personagem):
            alvo.life += self.__defesa
            print(f"{alvo.name} agora tem {alvo.life} de vida por ter equipado {self.name}")
        else:
            super().usar(alvo)

class Pocao(Item):
    def __init__(self, name, descricao, cura):
        super().__init__(name, descricao)
        self.__cura = cura
    
    @property
    def cura(self):
        return self.__cura
    
    @cura.setter
    def cura(self, novo):
        if novo >= 0:
            self.__cura = novo
    
    def usar(self, alvo):
        if isinstance(alvo, Personagem):
            alvo.life += self.__cura
            print(f"Personagem {alvo.name} curou {self.__cura}")
            print(f"Vida atual de: {alvo.name} quantia: {alvo.life}")
        else:
            super().usar(alvo)