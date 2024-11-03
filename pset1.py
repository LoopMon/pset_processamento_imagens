# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo: João Lucas da Costa
#    Matrícula: 202203331
#    Turma: CC5N
#    Email: jolucascosta05@gmail.com
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.


# Imports permitidos (não utilize nenhum outro import!):
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage


class Imagem:
    def __init__(self, largura, altura, pixels):
        """
        Inicializa uma imagem com largura, altura e lista de pixels.
        
        Parâmetros:
        largura (int): Largura da imagem.
        altura (int): Altura da imagem.
        pixels (list[int]): Lista linear de pixels que representa a imagem.
        """
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    def get_pixel(self, x, y):
        """
        Retorna o valor do pixel na posição (x, y), tratando bordas.
        
        Parâmetros:
        x (int): Coordenada x do pixel.
        y (int): Coordenada y do pixel.

        Retorna:
        int: Valor do pixel ajustado para tratar bordas da imagem.
        """
        # Tratamento para coordenadas fora dos limites
        if x < 0:
            x = 0
        elif x >= self.largura: 
            x = self.largura - 1
        if y < 0:
            y = 0
        elif y >= self.altura:
            y = self.altura - 1

        # Cálculo da posição na lista de pixels
        pos = self.largura * y + x 
        return self.pixels[pos]

    def set_pixel(self, x, y, c):
        """
        Define o valor de um pixel na posição (x, y).
        
        Parâmetros:
        x (int): Coordenada x do pixel.
        y (int): Coordenada y do pixel.
        c (int): Novo valor do pixel.
        """
        # Cálculo da posição na lista de pixels
        pos = self.largura * y + x 
        self.pixels[pos] = c

    def aplicar_por_pixel(self, func):
        """
        Aplica uma função a cada pixel da imagem, retornando uma nova imagem.
        
        Parâmetros:
        func (function): Função que recebe um pixel e retorna o valor transformado.

        Retorna:
        Imagem: Nova imagem com a função aplicada a cada pixel.
        """
        resultado = Imagem.nova(self.largura, self.altura)

        nova_cor = ""
        for x in range(0, resultado.largura):
            for y in range(0, resultado.altura):
                cor = self.get_pixel(x, y)
                nova_cor = func(cor)
                resultado.set_pixel(x, y, nova_cor)

        return resultado

    def invertida(self):
        """
        Retorna uma nova imagem com cores invertidas.

        Retorna:
        Imagem: Imagem com cores invertidas.
        """
        return self.aplicar_por_pixel(lambda c: 255 - c)
    
    def corrigir_pixel(self, pixel):
        """
        Corrige o valor de um pixel para estar entre 0 e 255.
        
        Parâmetros:
        pixel (float): Valor do pixel a ser corrigido.

        Retorna:
        int: Valor do pixel corrigido.
        """
        pixel = round(pixel)
        if pixel >= 255:
            return 255
        if pixel <= 0:
            return 0
        
        return pixel
    
    def correlacao(self, kernel, corrigir_pixel=True):
        """
        Aplica uma operação de correlação na imagem com um kernel dado.
        
        Parâmetros:
        kernel (list[list[int]]): Matriz usada para a operação de correlação.
        corrigir_pixel (bool): Indica se os pixels devem ser corrigidos para estarem no intervalo [0, 255].

        Retorna:
        Imagem: Nova imagem resultante da aplicação da correlação.
        """
        resultado = Imagem.nova(self.largura, self.altura)
        kernel_dim = len(kernel)
        centro = kernel_dim // 2
        soma = 0
        for linha in range(resultado.altura):
            for coluna in range(resultado.largura):
                # Aplica o kernel ao redor do pixel (linha, coluna)
                soma = 0
                for linha_kernel in range(kernel_dim):
                    for coluna_kernel in range(kernel_dim):
                        posX = coluna + (coluna_kernel - centro)
                        posY = linha + (linha_kernel - centro)
                        cor = self.get_pixel(posX, posY)
                        soma += kernel[linha_kernel][coluna_kernel] * cor

                if corrigir_pixel:
                    soma = self.corrigir_pixel(soma)
                resultado.set_pixel(coluna, linha, soma)
                
        return resultado
    
    def gerar_kernel(self, n):
        """
        Gera um kernel de borramento de dimensão n x n com valores iguais.
        
        Parâmetros:
        n (int): Tamanho do kernel (sempre convertido para um número ímpar).

        Retorna:
        list[list[float]]: Kernel de tamanho n x n.
        """
        if n % 2 == 0:
            n += 1 # Garantir que o kernel seja de tamanho ímpar

        kernel = []
        valor_pixel = 1 / (n * n)
        for i in range(n):
            linha = [valor_pixel] * n
            kernel.append(linha)

        return kernel[:]
        
    def borrada(self, n):
        """
        Aplica um efeito de desfoque na imagem usando um kernel de tamanho n x n.
        
        Parâmetros:
        n (int): Tamanho do kernel de desfoque.

        Retorna:
        Imagem: Imagem borrada.
        """
        kernel = self.gerar_kernel(n)
        resultado = self.correlacao(kernel)

        return resultado

    def focada(self, n):
        """
        Aumenta a nitidez da imagem aplicando um filtro de foco.
        
        Parâmetros:
        n (int): Tamanho do kernel de desfoque usado na operação de foco.

        Retorna:
        Imagem: Imagem com foco aumentado.
        """

        resultado = Imagem.nova(self.largura, self.altura)
        imagem_borrada = self.borrada(n)
        for linha in range(self.altura):
            for coluna in range(self.largura):
                # Aumenta a nitidez subtraindo a imagem borrada
                cor_imagem = self.get_pixel(coluna, linha) * 2
                cor_imagem_borrada = imagem_borrada.get_pixel(coluna, linha)
                cor = cor_imagem - cor_imagem_borrada
                cor = self.corrigir_pixel(cor)
                resultado.set_pixel(coluna, linha, cor)

        return resultado
    
    def bordas(self):
        """
        Detecta bordas na imagem usando os operadores de Sobel.
        
        Retorna:
        Imagem: Imagem realçada para mostrar as bordas.
        """
        kernel_X = [
            [1, 0, -1],
            [2, 0, -2],
            [1, 0, -1]
        ]
        kernel_Y = [
            [1, 2, 1],
            [0, 0, 0],
            [-1, -2, -1]
        ]

        resultado = Imagem.nova(self.largura, self.altura)
        imagem_kernel_X = self.correlacao(kernel_X, corrigir_pixel=False)
        imagem_kernel_Y = self.correlacao(kernel_Y, corrigir_pixel=False)

        combinacao = 0
        # Combina os resultados dos kernels X e Y
        for linha in range(self.altura):
            for coluna in range(self.largura):
                cor_imagem_x = imagem_kernel_X.get_pixel(coluna, linha)
                cor_imagem_y = imagem_kernel_Y.get_pixel(coluna, linha)

                combinacao = self.corrigir_pixel(math.sqrt(cor_imagem_x**2 + cor_imagem_y**2))
                resultado.set_pixel(coluna, linha, combinacao)
        
        return resultado
    
    
    # Abaixo deste ponto estão utilitários para carregar, salvar e mostrar
    # as imagens, bem como para a realização de testes. Você deve ler as funções
    # abaixo para entendê-las e verificar como funcionam, mas você não deve
    # alterar nada abaixo deste comentário.
    #
    # ATENÇÃO: NÃO ALTERE NADA A PARTIR DESTE PONTO!!! Você pode, no final
    # deste arquivo, acrescentar códigos dentro da condicional
    #
    #                 if __name__ == '__main__'
    #
    # para executar testes e experiências enquanto você estiver executando o
    # arquivo diretamente, mas que não serão executados quando este arquivo
    # for importado pela suíte de teste e avaliação.
    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem do arquivo fornecido e retorna uma instância dessa
        classe representando essa imagem. Também realiza a conversão para tons
        de cinza.

        Invocado como, por exemplo:
           i = Imagem.carregar('test_images/cat.png')
        """
        with open(nome_arquivo, 'rb') as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            l, a = img.size
            return cls(l, a, pixels)

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

        Invocado como, por exemplo:
            i = Imagem.nova(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, nome_arquivo, modo='PNG'):
        """
        Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo.
        Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será
        inferido a partir do nome fornecido. Se nome_arquivo for fornecido como
        um objeto semelhante a um arquivo, o tipo de arquivo será determinado
        pelo parâmetro 'modo'.
        """
        saida = PILImage.new(mode='L', size=(self.largura, self.altura))
        saida.putdata(self.pixels)
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)
        else:
            saida.save(nome_arquivo, modo)
        saida.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem
        fornecida, como uma imagem GIF.

        Função utilitária para tornar show_image um pouco mais limpo.
        """
        buffer = BytesIO()
        self.salvar(buffer, modo='GIF')
        return base64.b64encode(buffer.getvalue())

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se Tk não foi inicializado corretamente, não faz mais nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # O highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evento de redimensionamento (causando um loop infinito de
        # redimensionamento). Para maiores informações, ver:
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        tela = tkinter.Canvas(toplevel, height=self.altura,
                              width=self.largura, highlightthickness=0)
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        def ao_redimensionar(event):
            # Lida com o redimensionamento da imagem quando a tela é redimensionada.
            # O procedimento é:
            #  * converter para uma imagem PIL
            #  * redimensionar aquela imagem
            #  * obter os dados GIF codificados em base 64 (base64-encoded GIF data)
            #    a partir da imagem redimensionada
            #  * colocar isso em um label tkinter
            #  * mostrar a imagem na tela
            nova_imagem = PILImage.new(mode='L', size=(self.largura, self.altura))
            nova_imagem.putdata(self.pixels)
            nova_imagem = nova_imagem.resize((event.width, event.height), PILImage.NEAREST)
            buffer = BytesIO()
            nova_imagem.save(buffer, 'GIF')
            tela.img = tkinter.PhotoImage(data=base64.b64encode(buffer.getvalue()))
            tela.configure(height=event.height, width=event.width)
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        # Por fim, faz o bind da função para que ela seja chamada quando a tela
        # for redimensionada:
        tela.bind('<Configure>', ao_redimensionar)
        toplevel.bind('<Configure>', lambda e: tela.configure(height=e.height, width=e.width))

        # Quando a tela é fechada, o programa deve parar
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


# Não altere o comentário abaixo:
# noinspection PyBroadException
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()


    def refaz_apos():
        tcl.after(500, refaz_apos)


    tcl.after(500, refaz_apos)
except:
    tk_root = None

WINDOWS_OPENED = False

if __name__ == '__main__':
    # O código neste bloco só será executado quando você executar
    # explicitamente seu script e não quando os testes estiverem
    # sendo executados. Este é um bom lugar para gerar imagens, etc.
    help(Imagem)

    # O código a seguir fará com que as janelas de Imagem.mostrar
    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
