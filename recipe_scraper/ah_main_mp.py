from mp_ah_recep_fetcher import create_list, fetch_receps
import multiprocessing as mp


recep_list = create_list()
with mp.Pool() as p:
    p.map(fetch_receps, recep_list)
