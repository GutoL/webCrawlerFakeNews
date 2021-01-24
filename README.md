# webCrawlerFakeNews
Web crawler escrito em python para extração de fake news sobre a COVID-19 no site: https://piaui.folha.uol.com.br/lupa/

O crawler busca as informações sobre fake news do site e salva um data frame com as seguintes informações das fake news:

*Data: Data em que a notícia foi publicada no site;<br>
*URL: url para a postagem sobre a fake news;<br>
*Texto: texto que descreve a notícia;<br>
*Fonte: mostra onde a notícia estava sendo publicada (whatsapp, facebook, etc.);<br>
*Classificação: o site lupa, ao avaliar cada notícia, as classifica em diferentes categorias (falso, exagerado, contraditório, etc). Para mais informações, clique [aqui](https://piaui.folha.uol.com.br/lupa/2015/10/15/como-fazemos-nossas-checagens/);<br>
*Link da imagem: as notícias eventualmente são publicadas em formato de imagem nas redes sociais, esse campo mostra o link para a referida imagem; e<br>
*JSON: JSON com o resumo de toda as informações que são publicadas no site

