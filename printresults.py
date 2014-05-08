def print_results(results, sample_vars):
    print('Sample ' + sample_vars['Sample'] + ' results: \n' + 'X:' + str(results['XPeaks']).strip('[]') + '\n')
    if sample_vars['Y']: 
        print('Y:' + str(results['YPeaks']).strip('[]') + '\n')

