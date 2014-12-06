find_user_query = "SELECT * FROM users WHERE email = %s"
new_user_query = "INSERT INTO users (email, pass) VALUES (%s, %s)"
folio_stocks_query = "SELECT s.ticker FROM portfolio_stocks s WHERE s.userid=%s and s.folioid=%s"