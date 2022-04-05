
def name_col(p,in_):
    ind_row = p - in_ + 1
    index_ = list()
    for cin in range(ind_row):
        index_.append(f"open_{cin}")
        index_.append(f"high_{cin}")
        index_.append(f"low_{cin}")
        index_.append(f"close_{cin}")
        index_.append(f"mart_{cin}")
        index_.append(f"mart_inv_{cin}")
        index_.append(f"ampl_1{cin}")
        index_.append(f"ampl_2{cin}")
    return index_
    # extracted from https://programmerclick.com/article/34731200625/
def RSI(t, periods=10):
    length = len(t)
    rsies = [np.nan]*length
         # La longitud de los datos no excede el período y no se puede calcular;
    if length <= periods:
        return rsies
         #Utilizado para cálculos rápidos;
    up_avg = 0
    down_avg = 0
 
         # Primero calcule el primer RSI, use los períodos anteriores + 1 dato para formar una secuencia de períodos;
    first_t = t[:periods+1]
    for i in range(1, len(first_t)):
                 #Precio aumentado;
        if first_t[i] >= first_t[i-1]:
            up_avg += first_t[i] - first_t[i-1]
                 #caída de los precios; 
        else:
            down_avg += first_t[i-1] - first_t[i]
    up_avg = up_avg / periods
    down_avg = down_avg / periods
    rs = up_avg / down_avg
    rsies[periods] = 100 - 100/(1+rs)

    return rsies