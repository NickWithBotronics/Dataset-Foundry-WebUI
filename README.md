# Dataset-Foundry
Create Alpaca Formated Datasets to train LLM, get price estimates, format your dataset. HUGE WIP

In order to run change Upload folder direrctory in line 10 of your Main.py

Requirements:
pip install flask openai werkzeug

To run do: py main.py

Currently only the pricing estimate works. 

The factor is the assumption that your generated dataset will cost an X amount times more in tokens so you can set the factor. Lets do 3 for now, may vary depending on your prompt (edit in main.py). If the dataset is made up of 20,000,000 million tokens worth of questions then we will have to generate 60,000,000 million tokens. It will show as such: "The cost for 20000000 tokens using gpt3.5t is $120.00" even though it is factoring 3 times more tokens it stil says 20,000,000, but the price changes, so if we were to caculate it with no factor we would get a very bas estimate: "The cost for 20000000 tokens using gpt3.5t is $40.00"

![Screenshot 2023-06-11 194508](https://github.com/NickWithBotronics/Dataset-Foundry/assets/122953474/d0d162b7-c97c-4d46-8a10-af6f6aa2dcea)


TODO:
Create option to save formated dataset 
Get formatted datasets to work 
Get foundry section to work 
Have a section that shows the api answering questions.
