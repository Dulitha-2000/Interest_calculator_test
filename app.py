from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        loan_amount = float(request.form['loan_amount'].replace(",", ""))
        loan_term_years = int(request.form['loan_term_years'])
        loan_term_months = int(request.form['loan_term_months'])
        interest_rate = float(request.form['interest_rate']) / 100
        compound_frequency = request.form['compound']

        total_months = (loan_term_years * 12) + loan_term_months

        if compound_frequency == "Monthly (APR)":
            monthly_rate = interest_rate / 12
        else:
            return render_template('index.html', error="Currently only Monthly (APR) is supported.")

        if total_months == 0:
            return render_template('index.html', error="Loan term cannot be zero.")

        monthly_payment = (loan_amount * monthly_rate) / (1 - (1 + monthly_rate) ** -total_months)
        return render_template('index.html', monthly_payment=f"${monthly_payment:.2f}")
    except ValueError:
        return render_template('index.html', error="Please enter valid numerical values.")

if __name__ == '__main__':
    app.run(debug=True)
