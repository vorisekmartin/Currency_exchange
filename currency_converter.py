# API usage - https://github.com/hakanensari/fixer-io - http://fixer.io/
# zaverzované .idea


# nesmyslné pořadí importů
from grab import Grab
import json
import argparse

# argparse patří minimálně do __name__ bloku
argparser = argparse.ArgumentParser()
argparser.add_argument("--amount", type=float, default=1)
argparser.add_argument("--input_currency", type=str, default='EUR')
argparser.add_argument("--output_currency", type=str)
argv = argparser.parse_args()


# pouze jedna funkce
def main():
    # overkill
    g = Grab()
    # L24-L27 je nepřehledný kus kódu + použití \ == použítí oneline řešení na problém, který se na jeden řádek nevejde
    # nepoužití urlencode
    resp = g.go('http://api.fixer.io/latest?base={input}&symbols={output}'.format(input=argv.input_currency,
                                                                                  output=argv.output_currency)) \
        if argv.output_currency is not None else g.go(
        'http://api.fixer.io/latest?base={input}'.format(input=argv.input_currency))
    # g.response.json
    js = json.loads(resp.body)

    result = {}
    result["input"] = {"amount": argv.amount, "currency": argv.input_currency}
    result["output"] = {}
    for x in js["rates"]:
        result["output"][x] = float(js["rates"][x]) * argv.amount
    print(json.dumps(result, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()
