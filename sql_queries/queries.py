find_user_query = "SELECT * FROM users WHERE email = %s"
new_user_query = "INSERT INTO users (email, pass) VALUES (%s, %s)"
folio_stocks_query = "SELECT s.ticker, s.name, s.dataset, s.startdate" \
                     " FROM portfolio_stocks ps, stocks s " \
                     "WHERE ps.userid=%s and ps.folioid=%s and ps.dataset = s.dataset"
match_stock = "SELECT s.ticker, s.name, s.dataset, s.startdate" \
              " FROM stocks s" \
              " WHERE s.ticker Like %s Or s.name Like %s"
all_stocks = "Select s.ticker, s.name, s.dataset, s.startdate From stocks s"