from lxml import etree
from google.colab import files
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

def upload_file():
  uploaded = files.upload()

  nome_arquivo = list(uploaded.keys())[0]

  tree = etree.parse(nome_arquivo)
  root = tree.getroot()

  print("Raiz:", root.tag)

  nsmap = root.nsmap
  print(nsmap)
  return root

def ler_dados(root):
  if None in root.nsmap:
      ns = {'ns': root.nsmap[None]}
  else:
      ns = root.nsmap

  tags_medicoes = ['Vx', 'Ix', 'f', 'PF', 'DF', 'Cp']

  dados = {}

  for tag in tags_medicoes:

      elementos = root.xpath(f'.//ns:{tag}', namespaces=ns)

      valores = []

      for elem in elementos:
          valor = elem.find('.//ns:dValue', namespaces=ns)

          if valor is not None:
              try:
                  valores.append(float(valor.text.replace(",", ".")))
              except:
                  pass

      dados[tag] = valores

  df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in dados.items()]))

  # Lista das tags que você quer extrair
  tags = [
      "Cref", "DFref", "DeltaC", "DeltaDF",
      "CTratio", "K", "Toil", "Tamb"
  ]

  dados = []

  cards = root.xpath('.//ns:Cards_Item', namespaces=ns)

  for card in cards:
      
      linha = {}
      
      # Nome do ensaio (bstrName)
      nome = card.find('.//ns:bstrName', namespaces=ns)
      linha["Card"] = nome.text if nome is not None else None
      
      # Extrair cada tag
      for tag in tags:
          elemento = card.find(f'.//ns:{tag}/ns:dValue', namespaces=ns)
          linha[tag] = float(elemento.text) if elemento is not None else None
      
      dados.append(linha)

  # Criar dataframe
  df_config = pd.DataFrame(dados)

  df['Cp'] = df['Cp']*1e12
  df['Ix'] = df['Ix']*1e3

  display(df_config)
  display(df)

  return df, df_config

def plotar_capacitancia(df, df_config, y_min=None, y_max=None):
  f_min = df['f'].min()
  f_max = df['f'].max()
  plt.figure(figsize=(10, 3))

  if y_min is not None and y_max is not None:
    plt.ylim(y_min, y_max)

  if y_min is not None and y_max is None:
    plt.ylim(y_min, df['Cp'].max())

  if y_min is None and y_max is not None:
    plt.ylim(df['Cp'].min(), y_max)

  plt.xlim(f_min, f_max)
  plt.axvline(x=60, linestyle='--', linewidth=2, color='red')
  plt.text(70, df['Cp'].max(), '  60 Hz', horizontalalignment='center')
  plt.xlabel('f (Hz)')
  plt.ylabel('pF')
  plt.title('Capacitância - ' + df_config['Card'].iloc[0])
  plt.grid(True)
  plt.plot(df['f'], df['Cp'])
  plt.savefig("Cp.png", dpi=300, bbox_inches='tight')
  plt.show()

def plotar_FP(df, df_config, y_min=None, y_max=None):
  f_min = df['f'].min()
  f_max = df['f'].max()
  plt.figure(figsize=(10, 3))

  if y_min is not None and y_max is not None:
    plt.ylim(y_min, y_max)

  if y_min is not None and y_max is None:
    plt.ylim(y_min, df['PF'].max())

  if y_min is None and y_max is not None:
    plt.ylim(df['PF'].min(), y_max)

  plt.xlim(f_min, f_max)
  plt.axvline(x=60, linestyle='--', linewidth=2, color='red')
  plt.text(70, df['PF'].max(), '  60 Hz', horizontalalignment='center')
  plt.xlabel('f (Hz)')
  plt.ylabel('%')
  plt.title('Fator de Potência - ' + df_config['Card'].iloc[0])
  plt.grid(True)
  plt.plot(df['f'], df['PF'])
  plt.show()

def plotar_corrente(df, df_configdf, y_min=None, y_max=None):
  f_min = df['f'].min()
  f_max = df['f'].max()
  plt.figure(figsize=(10, 3))

  if y_min is not None and y_max is not None:
    plt.ylim(y_min, y_max)

  if y_min is not None and y_max is None:
    plt.ylim(y_min, df['Ix'].max())

  if y_min is None and y_max is not None:
    plt.ylim(df['Ix'].min(), y_max)

  plt.xlim(f_min, f_max)
  plt.axvline(x=60, linestyle='--', linewidth=2, color='red')
  plt.text(70, df['Ix'].max(), '  60 Hz', horizontalalignment='center')
  plt.xlabel('f (Hz)')
  plt.ylabel('mA')
  plt.title('Corrente - ' + df_config['Card'].iloc[0])
  plt.grid(True)
  plt.plot(df['f'], df['Ix'])

  plt.show()
