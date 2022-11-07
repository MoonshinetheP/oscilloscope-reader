import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def plot(input):
    with PdfPages (f'input.pdf') as pdf:
        fig = plt.figure(num = 1, figsize = (6.4,4.8), dpi = 100, facecolor = 'white', edgecolor = 'white', frameon = True)
        ax = fig.add_axes([0.2,0.2,0.7,0.7])
        ax.plot(x = input[0], y = input[1], linwidth = 1, linestyle = '-', color = 'red')

        pdf.savefig()
        plt.close()

