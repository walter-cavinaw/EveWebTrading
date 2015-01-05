find_user_query = "SELECT * FROM users WHERE email = %s"

new_user_query = "INSERT INTO users (email, pass) VALUES (%s, %s)"

folio_query = "SELECT * " \
              "FROM portfolios " \
              "WHERE userId=%s"

folio_all_stocks_query = "SELECT s.ticker, s.name, s.dataset, s.startdate" \
                     " FROM portfolio_stocks ps, stocks s " \
                     "WHERE ps.userid=%s and ps.dataset = s.dataset"

folio_stocks_query = "SELECT s.ticker, s.name, s.dataset, s.startdate" \
                     " FROM portfolio_stocks ps, stocks s " \
                     "WHERE ps.userid=%s AND ps.folioid=%s AND ps.dataset = s.dataset"

match_stock = "SELECT s.ticker, s.name, s.dataset, s.startdate" \
              " FROM stocks s" \
              " WHERE s.ticker Like %s OR s.name LIKE %s"

all_stocks = "Select s.ticker, s.name, s.dataset, s.startdate FROM stocks s"

add_stock_query = "Insert into portfolio_stocks values (%s, %s, %s)"