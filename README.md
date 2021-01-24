# webCrawlerFakeNews
Web crawler escrito em python para extração de fake news sobre a COVID-19 no site: https://piaui.folha.uol.com.br/lupa/

O crawler busca as informações sobre fake news do site e salva um data frame com as seguintes informações das fake news:

*Data: Data em que a notícia foi publicada no site;<br>
*Texto: texto que descreve a notícia;<br>
*Fonte: mostra onde a notícia estava sendo publicada (whatsapp, facebook, etc.);<br>
*Link da imagem: as notícias eventualmente são publicadas em formato de imagem nas redes sociais, esse campo mostra o link para a referida imagem; e<br>
*JSON: JSON com o resumo de toda as informações que são publicadas no site

