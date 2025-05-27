<template>
  <div class="book-home">
    <!-- 메인 카드 그리드 -->
    <main class="main-grid">
      <!-- 왼쪽: Book Club Episodes -->
      <section class="main-col col-left">
        <div class="section-title"><span>📖</span> Book Club Episodes</div>
        <div class="main-card card-episode">
          <div class="card-title">Discover the World of Books</div>
          <div class="card-row">
            <img class="avatar" src="https://randomuser.me/api/portraits/men/2.jpg" />
            <span class="card-label">Discover</span>
          </div>
          <div class="card-row">
            <img class="avatar" src="https://randomuser.me/api/portraits/women/3.jpg" />
            <span class="card-label">Bookworm</span>
          </div>
        </div>
        <div class="main-card">
          <img class="card-img" src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80" />
          <div class="card-caption">Heartwarming Story</div>
          <div class="card-title">Lost and Found: A Book's Journey</div>
          <div class="card-footer">Exciting Read · Discover a new world</div>
        </div>
      </section>

      <!-- 중앙: 메인 특집 -->
      <section class="main-col col-center">
        <div class="main-card card-featured">
          <img class="card-img" src="https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=400&q=80" />
          <div class="card-caption">Literary Treasures</div>
          <div class="card-title">Escape with Engaging Reads</div>
          <div class="card-desc">Immerse yourself in captivating stories and explore new worlds through the pages of a book.</div>
        </div>
      </section>

      <!-- 오른쪽: 추천/뉴스 -->
      <section class="main-col col-right">
        <div class="main-card">
          <img class="card-img" src="https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=400&q=80" />
          <div class="card-caption">Book Recommendations</div>
          <div class="card-title">Dive into a New Story</div>
          <div class="card-footer">Book Lover's Paradise · Book Discovery</div>
        </div>
        <div class="main-card">
          <img class="card-img" src="https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=400&q=80" />
          <div class="card-caption">Latest Book News</div>
          <div class="card-title">Explore the Book Universe</div>
          <div class="card-footer">Book Enthusiast · Bookworm Community</div>
        </div>
      </section>
    </main>

    <!-- Join the Book Club -->
    <section class="club-section">
      <div class="club-header">
        <h2>Join the Book Club</h2>
        <button class="join-btn join-now">Join Now</button>
      </div>
      <div class="club-grid">
        <div class="club-card">
          <img class="card-img" src="https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=400&q=80" />
          <div class="card-caption">Book Discussions</div>
          <div class="card-title">Discover the Best Books</div>
          <div class="card-footer">Book Mixologist · Latest Book News</div>
        </div>
        <div class="club-card">
          <img class="card-img" src="https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=400&q=80" />
          <div class="card-caption">Literary Delights</div>
          <div class="card-title">Find Hidden Gems</div>
          <div class="card-footer">Bookworm's Picks · Literary Explorer</div>
        </div>
        <div class="club-card">
          <img class="card-img" src="https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=400&q=80" />
          <div class="card-caption">Book Discoveries</div>
          <div class="card-title">Reading on a Budget</div>
          <div class="card-footer">Literary Explorer · Latest Book News</div>
        </div>
        <div class="club-card">
          <img class="card-img" src="https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=400&q=80" />
          <div class="card-caption">Affordable Reads</div>
          <div class="card-title">Mixing Book Mocktails</div>
          <div class="card-footer">Book Mixologist · Latest Book News</div>
        </div>
      </div>
    </section>

    <!-- Editor's Book Picks -->
    <section class="editor-section">
      <h2 class="editor-title">Editor's Book Picks</h2>
      <div class="editor-grid">
        <div class="editor-card">
          <span class="editor-rank">1</span>
          <img class="card-img" src="https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=400&q=80" />
          <div class="card-caption">Latest Book News</div>
          <div class="card-title">Book Lovers' Happiness</div>
          <div class="card-footer">Exciting Reads</div>
        </div>
        <div class="editor-card">
          <span class="editor-rank">2</span>
          <img class="card-img" src="https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=400&q=80" />
          <div class="card-caption">Book Enthusiasts</div>
          <div class="card-title">Get Ready for the Book Championship</div>
          <div class="card-footer">Bookworm Community</div>
        </div>
        <div class="editor-card">
          <span class="editor-rank">3</span>
          <img class="card-img" src="https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=400&q=80" />
          <div class="card-caption">Literary Delights</div>
          <div class="card-title">Experience the Magic of Books</div>
          <div class="card-footer">Book Club Fun</div>
        </div>
      </div>
    </section>

    <!-- 푸터 -->
    <footer class="footer-section">
      <div class="footer-row">
        <div class="footer-brand">
          <div class="footer-title">Book Community</div>
          <div class="footer-desc">Inspiring readers since 2018</div>
        </div>
        <div class="footer-col">
          <h4>Explore</h4>
          <ul>
            <li><a href="#">Our story</a></li>
            <li><a href="#">Opportunities</a></li>
            <li><a href="#">Get in touch</a></li>
            <li><a href="#">Articles</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Join the discussion</h4>
          <ul>
            <li><a href="#">Support Center</a></li>
            <li><a href="#">Join as Premium</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Connect with us</h4>
          <ul>
            <li><a href="#">Facebook</a></li>
            <li><a href="#">Twitter</a></li>
            <li><a href="#">Instagram</a></li>
          </ul>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
}
</script>

<style scoped>
.book-home {
  background: #fff;
  color: #181818;
  min-height: 100vh;
  font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
}
.main-header {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2.7rem 2vw 0.8rem 2vw;
  text-align: center;
}
.header-row {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 1.2rem;
  margin-bottom: 1.6rem;
}
.search-bar {
  flex: 1 1 350px;
  max-width: 350px;
  min-width: 180px;
  padding: 0.7rem 1.3rem;
  border: 1.5px solid #ececec;
  border-radius: 21px;
  font-size: 1.07rem;
  background: #fafafa;
  margin-right: auto;
}
.header-actions {
  display: flex;
  gap: 0.8rem;
}
.login-btn {
  background: none;
  border: 1.5px solid #888;
  color: #222;
  font-weight: 500;
  border-radius: 20px;
  padding: 0.45em 1.5em;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.16s, color 0.16s;
}
.login-btn:hover {
  background: #f5f5f5;
}
.join-btn {
  background: #7c3aed;
  color: #fff;
  border: none;
  border-radius: 20px;
  padding: 0.45em 1.5em;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.16s;
}
.join-btn:hover {
  background: #5b21b6;
}
.site-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 1.7rem;
  letter-spacing: -1px;
  line-height: 1.2;
}
.tab-nav {
  display: flex;
  justify-content: center;
  gap: 1.2rem;
  margin-bottom: 2.5rem;
  border-bottom: 1.5px solid #ececec;
  padding-bottom: 0.7rem;
}
.tab-link {
  color: #222;
  font-size: 1.04rem;
  font-weight: 500;
  padding: 0.4em 1.2em;
  border-radius: 14px 14px 0 0;
  background: none;
  cursor: pointer;
  border: none;
  transition: background 0.16s, color 0.16s;
}
.tab-link.active,
.tab-link:hover {
  background: #f5f5f5;
  color: #7c3aed;
}

.main-grid {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.1fr 1.3fr 1.1fr;
  gap: 2.2rem;
  margin-bottom: 2.7rem;
}
.main-col {
  display: flex;
  flex-direction: column;
  gap: 1.6rem;
}
.section-title {
  font-size: 1.13rem;
  font-weight: 700;
  margin-bottom: 0.7rem;
  display: flex;
  align-items: center;
  gap: 0.5em;
}
.main-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  padding: 1.2rem 1.2rem 1rem 1.2rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  position: relative;
  min-height: 120px;
}
.card-img {
  width: 100%;
  max-width: 100%;
  height: 120px;
  object-fit: cover;
  border-radius: 12px;
  margin-bottom: 0.7rem;
  background: #f5f5f5;
}
.card-episode .card-row {
  display: flex;
  align-items: center;
  gap: 0.7em;
  margin-bottom: 0.6em;
}
.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  background: #e0e0e0;
}
.card-label {
  font-size: 1.01rem;
  color: #7c3aed;
  font-weight: 600;
}
.card-caption {
  color: #888;
  font-size: 0.98rem;
  margin-bottom: 0.1rem;
  font-weight: 500;
}
.card-title {
  font-size: 1.13rem;
  font-weight: 700;
  margin-bottom: 0.2rem;
  color: #181818;
}
.card-desc {
  font-size: 1.01rem;
  color: #444;
  margin-bottom: 0.5rem;
}
.card-footer {
  font-size: 0.93rem;
  color: #888;
  margin-top: 0.3rem;
}

.club-section {
  max-width: 1200px;
  margin: 0 auto 2.7rem auto;
  padding-top: 2.3rem;
  border-top: 1.5px solid #ececec;
}
.club-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.3rem;
  gap: 1.5rem;
}
.club-header h2 {
  font-size: 1.23rem;
  font-weight: 700;
}
.club-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.4rem;
}
.club-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  padding: 1.1rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.club-card .card-img {
  height: 100px;
  margin-bottom: 0.6rem;
}
.club-card .card-caption {
  color: #888;
  font-size: 0.96rem;
  margin-bottom: 0.1rem;
}
.club-card .card-title {
  font-size: 1.07rem;
  font-weight: 700;
  margin-bottom: 0.2rem;
}
.club-card .card-footer {
  font-size: 0.92rem;
  color: #888;
  margin-top: 0.2rem;
}

.editor-section {
  max-width: 1200px;
  margin: 0 auto 2.7rem auto;
  padding-top: 2.3rem;
  border-top: 1.5px solid #ececec;
}
.editor-title {
  font-size: 1.23rem;
  font-weight: 700;
  margin-bottom: 1.3rem;
}
.editor-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.4rem;
}
.editor-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  padding: 1.1rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  position: relative;
}
.editor-card .editor-rank {
  position: absolute;
  left: 1.1rem;
  top: 1.1rem;
  font-size: 2.3rem;
  font-weight: 800;
  color: #e5e5e5;
  pointer-events: none;
  z-index: 1;
}
.editor-card .card-img {
  height: 100px;
  margin-bottom: 0.6rem;
  z-index: 2;
  position: relative;
}
.editor-card .card-caption {
  color: #888;
  font-size: 0.96rem;
  margin-bottom: 0.1rem;
}
.editor-card .card-title {
  font-size: 1.07rem;
  font-weight: 700;
  margin-bottom: 0.2rem;
}
.editor-card .card-footer {
  font-size: 0.92rem;
  color: #888;
  margin-top: 0.2rem;
}

.footer-section {
  background: #fafafa;
  border-top: 1px solid #ececec;
  padding: 2.2rem 0 1.7rem 0;
  font-size: 1rem;
  color: #888;
  margin-top: 2rem;
}
.footer-row {
  display: flex;
  flex-wrap: wrap;
  gap: 2.5rem;
  justify-content: center;
  margin-top: 1.2rem;
}
.footer-brand {
  min-width: 200px;
}
.footer-title {
  font-size: 1.12rem;
  font-weight: 700;
  color: #181818;
  margin-bottom: 0.5rem;
}
.footer-desc {
  font-size: 0.98rem;
  color: #888;
}
.footer-col {
  min-width: 180px;
}
.footer-col h4 {
  font-size: 1.05rem;
  font-weight: 700;
  color: #222;
  margin-bottom: 0.7rem;
}
.footer-col ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.footer-col li {
  margin-bottom: 0.5rem;
}
.footer-col a {
  color: #888;
  text-decoration: none;
  transition: color 0.15s;
}
.footer-col a:hover {
  color: #7c3aed;
}
.navbar {
  margin-bottom: 80px
}

/* 반응형 */
@media (max-width: 1100px) {
  .main-header, .main-grid, .club-section, .editor-section { max-width: 98vw; }
  .main-grid { gap: 1.2rem; }
  .club-grid, .editor-grid { gap: 1rem; }
}
@media (max-width: 900px) {
  .main-grid { grid-template-columns: 1fr; }
  .main-col { flex-direction: row; flex-wrap: wrap; gap: 1rem; }
  .main-card, .club-card, .editor-card { width: 100%; }
  .club-grid, .editor-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 600px) {
  .main-header, .main-grid, .club-section, .editor-section { padding-left: 0.5rem; padding-right: 0.5rem; }
  .site-title { font-size: 1.6rem; }
  .tab-nav { flex-wrap: wrap; gap: 0.5rem; }
  .club-grid, .editor-grid { grid-template-columns: 1fr; }
}
</style>
