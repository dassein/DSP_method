'''
calculate the cutoff frequency based on list_transient_band
freq_cutoff = ( freq_start + freq_end ) / 2 for transient band
'''

def calc_freq_cutoff(list_transient_band):
    list_freq_cutoff = []
    for [freq_start, freq_end] in list_transient_band:
        freq_cutoff = ( freq_start + freq_end ) / 2
        list_freq_cutoff.append( freq_cutoff )
    return list_freq_cutoff