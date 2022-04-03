
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