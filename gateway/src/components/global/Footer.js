import '../../styles/footer.css'

function Footer() {
    return (
      <footer>
        <div className="footer-row">
          <div className="footer-col">
            <h4>Info</h4>
            <ul className="links">
              <li><a href="#">About Us</a></li>
            </ul>
          </div>
          <div className="footer-col">
            <h4>Explore</h4>
            <ul className="links">
              <li><a href="#">Free Designs</a></li>
            </ul>
          </div>
          <div className="footer-col">
            <h4>Legal</h4>
            <ul className="links">
              <li><a href="#">Customer Agreement</a></li>
            </ul>
          </div>
          <div className="footer-col">
            <h4>Newsletter</h4>
            <p>
              Subscribe to our newsletter for a weekly dose
              of news, updates, helpful tips, and
              exclusive offers. 
            </p>
            <div className="icons">
              <i className="fa-brands fa-facebook-f"></i>
              <i className="fa-brands fa-twitter"></i>
              <i className="fa-brands fa-linkedin"></i>
              <i className="fa-brands fa-github"></i>
            </div>
          </div>
        </div>
      </footer>
    )
}

export default Footer