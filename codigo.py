from __future__ import annotations
from typing import Any
from dataclasses import dataclass

@dataclass
class No:
    '''
    Representa um nó de uma árvore. Contém uma chave (dado de
    algum tipo sujeito a uma relação de ordem), referências 
    para subárvore esquerda e subárvore direita e a altura. 
    '''
    chave: Any
    esquerda: No | None = None
    direita: No | None = None
    altura_atributo: int = 1

class ArvoreAVL:
    ''' Cria uma classe chamada 'ArvoreAVL' onde está presente funções
    que permitem fazer a inserção/remoção de modo que mantenha a árvore AVL (árvore Binária de Busca Balanceada) balanceada.
    Ainda respeita todas as regras de uma árvore binária de ter até 2 filhos, e a premissa da ABB, onde os filhos com 
    valor menor ficam a esquerda e os filhos com valores maiores que a raiz ficam a direita.
    '''

    def __init__(self):
        ''' Cria uma uma Árvore de Busca Binária Balanceada vazia '''
        self.raiz = None

    def vazia(self) -> bool:
        '''Verifica se a árvore está vazia, isto é, devolve True se não possui
        nenhum vértice; caso contrário, devolve False.
        Exemplos:
        >>> avl = ArvoreAVL()
        >>> avl.vazia()
        True
        >>> _ = avl.insere(10) #ignorando resultado booleano da operação
        >>> avl.vazia()
        False
        '''
        return self.raiz == None

    def altura(self, no: No | None) -> int:
        '''
        Calcula a altura de um **no** da árvore de forma recursiva, isto é, 
        o comprimento do maior caminho do **no** até um nó folha. 
        Caso o nó seja None, retorna -1.

        >>> arvore = ArvoreAVL()
        >>> for item in [50, 30, 20, 10, 40, 70, 60, 80, 90, 100]:
        ...     arvore.insere(item)
        >>> arvore.altura(arvore.raiz)
        3
        >>> arvore.altura(arvore.raiz.esquerda)
        1
        >>> arvore.altura(arvore.raiz.direita.esquerda)
        1

        '''
        if no is None:
            return -1
        return 1 + max(self.altura(no.esquerda), self.altura(no.direita))

    def fator_balanceamento(self, no: No) -> int:
        '''Calcula o fator de balanceamento de um nó. O fator de balanceamento de um nó é a diferença 
        entre as alturas das suas subárvores esquerda e direita (Fb = He - Hd).

        Exemplos:
        >>> avl = ArvoreAVL()
        >>> esquerda = No(5)
        >>> direita = No(15)
        >>> no = No(10, No(5), No(15))
        >>> avl.fator_balanceamento(no)
        0
        >>> no = No(10, No(5))
        >>> avl.fator_balanceamento(no)
        1
        >>> no = No(10, direita=No(15))
        >>> avl.fator_balanceamento(no)
        -1
        '''
        if no is None:
            return 0
        return self.altura(no.esquerda) - self.altura(no.direita)

    def rotacao_direita(self, no_raiz: No) -> No:
        '''
        Realiza uma rotação em torno do nó fornecido, essa rotação é à direita
        para balanciar a árvore.
        Exemplo desenho: 
        #      (30)                                             (20)
        #      /     | RSD(Rotação simples à direita)  ==>     /    \    (Rotacionado)     
        #    (20)    |                                        (10) (30)
        #   /        v 
        #  (10) 
        
        Exemplos:
        >>> avl = ArvoreAVL()
        >>> y = No(30)
        >>> y.esquerda = No(20)
        >>> y.esquerda.esquerda = No(10)
        >>> nova_raiz = avl.rotacao_direita(y)
        >>> nova_raiz.chave
        20
        >>> nova_raiz.direita.chave
        30
        >>> nova_raiz.esquerda.chave
        10
        '''
        no_centro = no_raiz.esquerda
        no_aux = no_centro.direita
        no_centro.direita = no_raiz
        no_raiz.esquerda = no_aux
        no_raiz.altura_atributo = 1 + max(self.altura(no_raiz.esquerda), self.altura(no_raiz.direita))
        no_centro.altura_atributo = 1 + max(self.altura(no_centro.esquerda), self.altura(no_centro.direita))
        return no_centro

    def rotacao_esquerda(self, no_raiz: No) -> No:
        '''
        Realiza uma rotação à esquerda em torno do nó fornecido,
        para balanciar a árvore.
        Exemplo desenho:  
        #       (10)                                          (20)                       
        #   |       \    RSE(Rotação simples à esquerda)     /    \     (Rotacionado)                          
        #   |      (20)                           ==>      (10)   (30)                               
        #   v     /    \                                      \                         
        #        (15)  (30)                                   (15)

        >>> avl = ArvoreAVL()
        >>> x = No(10)
        >>> x.direita = No(20)
        >>> x.direita.direita = No(30)
        >>> nova_raiz = avl.rotacao_esquerda(x)
        >>> nova_raiz.chave
        20
        >>> nova_raiz.esquerda.chave
        10
        >>> nova_raiz.direita.chave
        30
        '''
        no_centro = no_raiz.direita
        no_aux = no_centro.esquerda
        no_centro.esquerda = no_raiz
        no_raiz.direita = no_aux
        no_raiz.altura_atributo = 1 + max(self.altura(no_raiz.esquerda), self.altura(no_raiz.direita))
        no_centro.altura_atributo = 1 + max(self.altura(no_centro.esquerda), self.altura(no_centro.direita))
        return no_centro


    def insere(self, chave: Any) -> None:
        '''
        Faz a inserção do valor "chave" como um nó na árvore AVL, isso
        respeitando a premissa de elementos com o valor do no menor que a raiz
        a esquerda, e a direita valores o no.chave maior que a raiz. 

        Exemplos:
        >>> avl = ArvoreAVL()
        >>> avl.insere(10)
        >>> avl.exibe_pre_ordem()
        '(10)'
        >>> avl.insere(20)
        >>> avl.exibe_pre_ordem()
        '(10 (20))'
        >>> avl.insere(5)
        >>> avl.exibe_pre_ordem()
        '(10 (5) (20))'
        >>> avl.insere(15)
        >>> avl.exibe_pre_ordem()
        '(10 (5) (20 (15)))'
        >>> avl.insere(25)
        >>> avl.exibe_pre_ordem()
        '(10 (5) (20 (15) (25)))'

        '''
        self.raiz = self._insere(self.raiz, chave)

    def _insere(self, no: No | None, chave: Any) -> No:
        '''
        Verifica se o elemento é maior que o Nó, caso seja, adiciona á direita
        caso contrário adicona na esquerda. Atualiza a altura, e caso necessário, realiza rotação.
    
        '''
        if no is None:
            return No(chave)
        if chave < no.chave:
            no.esquerda = self._insere(no.esquerda, chave)
        else:
            no.direita = self._insere(no.direita, chave)

            
        no.altura_atributo = 1 + max(self.altura(no.esquerda), self.altura(no.direita))
        balanceamento = self.fator_balanceamento(no)
 
        if balanceamento > 1:
            if chave < no.esquerda.chave:
                return self.rotacao_direita(no)
            else:
                no.esquerda = self.rotacao_esquerda(no.esquerda)
                return self.rotacao_direita(no)

        if balanceamento < -1:
            if chave > no.direita.chave:
                return self.rotacao_esquerda(no)
            else:
                no.direita = self.rotacao_direita(no.direita)
                return self.rotacao_esquerda(no)

        return no


    def remove(self, chave: Any) -> None:
        '''
        Remove uma chave da árvore AVL.

        Exemplos:
        >>> avl = ArvoreAVL()
        >>> avl.insere(10)
        >>> avl.insere(5)
        >>> avl.insere(12)
        >>> avl.exibe_pre_ordem()
        '(10 (5) (12))'
        >>> avl.remove(5)
        >>> avl.exibe_pre_ordem()
        '(10 (12))'
        >>> avl.buscar(5) is None
        True
        >>> avl.remove(10)
        >>> avl.exibe_pre_ordem()
        '(12)'
        >>> avl.buscar(10) is None
        True
        '''
        self.raiz = self._remove(self.raiz, chave)

    def _remove(self, no: No | None, chave: Any) -> No | None:
        '''
        Função que efetua a remoção do nó contendo **chave** na subárvore 
        com raiz **no**. Atualiza a altura dos nós, e caso desbalanceia 
        chama as funções de rotação esquerda ou direita. 
        '''

        if no is None :
            return no
        if chave < no.chave:
            no.esquerda = self._remove(no.esquerda, chave)
        elif chave > no.chave:
            no.direita = self._remove(no.direita, chave)
        else:
            if no.esquerda == None:
                return no.direita
            elif no.direita == None:
                return no.esquerda
            temp = self.__sucessor(no.direita)
            no.chave = temp.chave
            no.direita = self._remove(no.direita, temp.chave)
        no.altura_atributo = 1 + max(self.altura(no.esquerda), self.altura(no.direita))
        balanceamento = self.fator_balanceamento(no)
        


        if balanceamento > 1:
            if self.fator_balanceamento(no.esquerda) >= 0:
                return self.rotacao_direita(no)
            else:
                no.esquerda = self.rotacao_esquerda(no.esquerda)
                return self.rotacao_direita(no)
        
        if balanceamento < -1:
            if self.fator_balanceamento(no.direita) <= 0:
                return self.rotacao_esquerda(no)
            else:
                no.direita = self.rotacao_direita(no.direita)
                return self.rotacao_esquerda(no)
        
        return no


    def buscar(self, elemento: Any) -> No | None:
        '''
        Devolve o nó contendo o "elemento" se estiver na subárvore 
        enraizada pela raiz da árvore AVL, caso contrário, devolve None.

        Exemplos:
        >>> avl = ArvoreAVL()
        >>> avl.insere(8)
        >>> avl.insere(17)
        >>> avl.insere(4)
        >>> no = avl.buscar(4)
        >>> no.chave
        4
        >>> no = avl.buscar(17)
        >>> no.chave
        17
        >>> avl.buscar(13) == None
        True
        >>> avl.buscar(10) == None
        True
        >>> avl.buscar(9) == None
        True
        '''
        return self._buscar(self.raiz, elemento)

    def _buscar(self, no: No | None, elemento: Any) -> No | None:
        if no == None or no.chave == elemento:
            return no
        else:
            if elemento < no.chave:
                return self._buscar(no.esquerda, elemento)
            else: 
                return self._buscar(no.direita, elemento)



    def __sucessor(self, no: No) -> No | None:
        '''
        Devolve o sucessor de um **no**, isto é, o nó com o menor valor
        maior (ou igual) ao valor de no.chave. 
    
        Exemplos:
        >>> arvore = ArvoreAVL()
        >>> for item in [50, 30, 70, 20, 40, 60, 80, 10, 35, 65]:
        ...     arvore.insere(item)
        >>> no = arvore._ArvoreAVL__sucessor(arvore.raiz)
        >>> no.chave
        60
        >>> no = arvore._ArvoreAVL__sucessor(arvore.raiz.esquerda)
        >>> no.chave
        35
        >>> no = arvore._ArvoreAVL__sucessor(arvore.raiz.direita)
        >>> no.chave
        80
        >>> no = arvore._ArvoreAVL__sucessor(arvore.raiz.direita.direita)
        >>> no == None
        True
        '''
        if no is None:
            return None
        
        if no.direita != None:
            return self.__minimo(no.direita)
        
        atual = self.raiz
        sucessor = None
        while atual is not None:
            if no.chave < atual.chave:
                sucessor = atual
                atual = atual.esquerda
            elif no.chave > atual.chave:
                atual = atual.direita
            else:
                atual = None  

        return sucessor

    def __minimo(self, no: No) -> No:
        '''
        Essa função serve para verificar o menor valor de um "no", que sera a raiz do momento, 
        isso para calcular o sucessor de um nó. Ou seja, como o sucessor deve ser procurado a 
        direita do no enraizado, a função retorna o menor valor, verificando os menores valores,
        que estão a esquerda do no. 
        '''
        while no.esquerda != None:
            no = no.esquerda
        return no
    
# problema escolhido 
    def k_esimo_maior(self, k: int) -> Any | None:
        '''
        A função é responsável por retornar o meior k-ésimo valor da função.
        Para isso chama uma sub-função "_k_esimo_maior", que recursivamente, verifica 
        e retorna o maior k-ésimo maior no. 
        Exemplos:
        >>> avl = ArvoreAVL()
        >>> avl.insere(9)
        >>> avl.insere(4)
        >>> avl.insere(88)
        >>> avl.insere(19)
        >>> avl.insere(14)
        >>> avl.insere(29)
        >>> avl.insere(49)
        >>> avl.k_esimo_maior(1)
        88
        >>> avl.k_esimo_maior(2)
        49
        >>> avl.k_esimo_maior(3)
        29
        >>> avl.k_esimo_maior(4)
        19
        >>> avl.k_esimo_maior(5)
        14
        >>> avl.k_esimo_maior(6) 
        9
        >>> avl.k_esimo_maior(7) 
        4
        >>> avl.k_esimo_maior(8) is None
        True
        >>> avl.k_esimo_maior(9) is None
        True
        >>> avl.k_esimo_maior(10) is None
        True
        '''
        self.contador = 0
        self.resultado = None
        self._k_esimo_maior(self.raiz, k)
        return self.resultado


    def _k_esimo_maior(self, no: No | None, k: int):
        '''
        A função verifica qual é o menor entre os maiores valores à 
        direita da raiz, que foi passada. 
        '''
        if no is None:
            return no

        if self.contador >= k:
            return no
        self._k_esimo_maior(no.direita, k)

        if self.contador < k:
            self.contador += 1

            if self.contador == k:
  
                self.resultado = no.chave
                return no
            else:        
                self._k_esimo_maior(no.esquerda, k)
        return no


    def exibe_pre_ordem(self) -> str:
        '''
        Retorna a árvore em pré-ordem que consciste em mostrar priemiro 
        a raiz da árvore, após isso mostra o filho à esquerda da raiz, e por fim 
        o filho a direita da raiz ex: (RAIZ(f_ESQUERDO)(f_DIREITO)).
        Exemplos: 
        >>> avl = ArvoreAVL()
        >>> avl.insere(10)
        >>> avl.insere(5)
        >>> avl.insere(15)
        >>> avl.exibe_pre_ordem()
        '(10 (5) (15))'
        >>> avl2 = ArvoreAVL()
        >>> avl2.insere(2)
        >>> avl2.insere(1)
        >>> avl2.insere(3)
        >>> avl2.exibe_pre_ordem()
        '(2 (1) (3))'
        '''
        return self._exibe_pre_ordem(self.raiz)

    def _exibe_pre_ordem(self, raiz: No | None) -> str:
        repr = ''
        if raiz != None:
            repr += '(' + str(raiz.chave)
            if raiz.esquerda != None:
                repr += ' ' + self._exibe_pre_ordem(raiz.esquerda)
            if raiz.direita != None:
                repr += ' ' + self._exibe_pre_ordem(raiz.direita)
            repr += ')'
        return repr 