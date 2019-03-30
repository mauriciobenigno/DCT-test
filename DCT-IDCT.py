import numpy as np
import math
from PIL import Image

matriz=np.array([[172,179,188,191,196,200,204,174],
                 [188,187,190,193,199,201,187,101],
                 [189,189,196,197,199,183,117, 84],
                 [186,192,197,199,189,130, 85, 85],
                 [198,197,199,192,149,100,100, 95],
                 [195,195,193,158,108, 98, 96, 98],
                 [195,189,171,111,111,108,104, 96],
                 [192,177,124,110,113,113,108,100]])

# -------- [ ZEROS ] -------- 
def InsereZerosZigZag(M,n):
    n=n-1
    n=63-n
    contador=0
    for i in range(M.shape[0]): 
        for j in range(M.shape[1]): 
            sum=i+j 
            if(sum%2 ==0): 
                if contador > n:
                    M[i][j] = 0
            else: 
                if contador > n:
                    M[i][j] = 0
            contador=contador+1
    return M
# -------- [ Contatenar Matrizes ] --------

def JuntaMatriz512(M):
    contador1=0 # Coluna atual da Matriz de saida
    contador2=0 # Coluna atual da matriz de saida
    contador3=0 # Numero de acesso a Matriz de entrada
    contador4=0 # Coluna atual da Matriz N de entrada
    Super=0
    G = np.zeros((512,512))
    for i in range(0, 512): # Quantidade de linhas
        for j in range(0,64): # quantidade de matrizes por linha
            for l in range(0,8): # quantidade de elementro por linha da matriz
                G[contador2,contador1]=M[j+contador3][contador4,l]
                #print("G["+str(contador2)+","+str(contador1)+"] = "+str(G[contador2,contador1])+" pois  M["+str(j+contador3)+"]["+str(contador4)+","+str(l)+"] = "+str(M[j+contador3][contador4,l]))
                contador1=contador1+1 #Incrementa ate 512 colunas       
        if (contador2+1)%8==0 and contador2!=0: # Metade das linhas da matriz de saida
            contador3=contador3+64
            #print("INCREMENTO -> "+str(contador3))
        contador2=contador2+1 #Incrementa até 512 linhas
        contador4=contador4+1 #incrementa até 8 linhas
        if contador4==8: #Verifica se contador 4 chegou a 8 linhas
            contador4=0 # retorna o valor a 0
        contador1=0
        Super=Super+1
    return G

# -------- [ DCT ] -------- 
def SomaX(n,u,v,y):
    somatorio = 0.0
    for x in range(0, 8):
        somatorio=somatorio+matriz[x][y]\
        *(math.cos((((2*x+1)*(u*math.pi)/16)))\
        *math.cos((((2*y+1)*(v*math.pi))/16)))
    return somatorio

def SomaY(n,u,v):
    somatorio = 0.0
    for y in range(0, 8):
        somatorio=somatorio+SomaX(n,u,v,y)
    return somatorio

def Cf(f):
    if f == 0:
        return (1/math.sqrt(2))
    else:
        return 1

def DCT(matriz,n):
    G = np.zeros((8,8))
    for u in range(0, 8):
        for v in range(0, n):
            G[u,v]=((Cf(u)/2)*(Cf(v)/2))*SomaY(n,u,v)
    return G


# -------- [ inverso DCT ] --------
def SomaV(M,n,x,y,u):
    somatorio = 0.0
    for v in range(0, 8):
        somatorio=somatorio+M[u][v]*((Cf(u)/2)*(Cf(v)/2))\
        *(math.cos(((2*x+1)*(u*math.pi)/16))\
        *math.cos(((2*y+1)*(v*math.pi))/16))
    return somatorio

def SomaU(M,n,x,y):
    somatorio = 0.0
    for u in range(0, 8):
        somatorio=somatorio+SomaV(M,n,x,y,u)
    return somatorio

def IDCT(M,n):
    G = np.zeros((8,8))
    for x in range(0, 8):
        for y in range(0, n):
            G[x,y]=SomaU(M,n,x,y)
    return G


def split(array, nrows, ncols):
    """Split a matrix into sub-matrices."""

    r, h = array.shape
    return (array.reshape(h//nrows, nrows, -1, ncols)
                 .swapaxes(1, 2)
                 .reshape(-1, nrows, ncols))

# -------- [ MAIN ] -------- 
def main():
    np.set_printoptions(suppress=True)
    print ("Matriz Original:")
    print (matriz)
    print (matriz.shape)

    aux=DCT(matriz,8)
    coeficienteDCT = InsereZerosZigZag(aux,54)
    print ("Matriz DCT:")
    print (coeficienteDCT)
    print (coeficienteDCT.shape)
    
    inversaDCT=IDCT(coeficienteDCT,8)
    inversaDCT=inversaDCT.astype(int)
    print ("Matriz Restaurada:")
    print (inversaDCT)
    print (inversaDCT.shape)


    '''print ("Matriz Original:")
    print (matriz)

    aux=DCT(matriz,8)
    coeficienteDCT = InsereZerosZigZag(aux,10)
    print ("Matriz DCT:")
    print (coeficienteDCT)
    

    inversaDCT=IDCT(coeficienteDCT,8)
    inversaDCT=inversaDCT.astype(int)
    
    print ("Matriz Restaurada:")
    print (inversaDCT)
    print (inversaDCT.shape)'''

    '''img = Image.open("lena_gray.bmp")

    A = np.array(img)

    # Divisão da Imagem em matrizes 8x8
    M = split(A,8,8)

    print ("Matriz Original:")
    print (M[0])

    coeficienteDCT=DCT(M[0],8)
    print ("Matriz DCT:")
    print (coeficienteDCT)

    inversaDCT=IDCT(coeficienteDCT,8)
    print ("Matriz Restaurada:")
    print (inversaDCT)
    print (inversaDCT.shape)'''
    '''N=M
    print ("Matriz:")
    print(M[0])
    for x in range(0, M.shape[0]):
        N[x] = DCT(M[x],8)

    print ("Matriz DCT:")
    print(N[0])
    O=N
    for x in range(0, N.shape[0]):
        O[x] = IDCT(N[x],8)

    print ("Matriz IDCT:")
    print(O[0])
    for x in range(0, M.shape[0]):
        N[x] = InsereZerosZigZag(N[x],64)
    IMG = JuntaMatriz512(O)

    B = Image.fromarray(IMG, mode=None)
    B.show()'''



if __name__ == "__main__":
    main()
    
    
    
