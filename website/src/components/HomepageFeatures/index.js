import React from "react";
import Link from "@docusaurus/Link";

export default function HeroSection() {
  return (
    <>
      {/* ================= HEADER ================= */}
      <header style={styles.header}>
        <div style={styles.navbar}>
          <div style={styles.logo}>SirAhsanKhan</div>
          <nav style={styles.navLinks}>
            <a href="#home" style={styles.navItem}>Home</a>
            <a href="#about" style={styles.navItem}>About</a>
            <a href="#contact" style={styles.navItem}>Contact</a>
          </nav>
        </div>
      </header>

      {/* ================= HERO SECTION ================= */}
      <section style={styles.hero}>
        <div style={styles.heroContent}>
          {/* Left Image */}
          <div style={{ ...styles.left, animation: "fadeInLeft 1s forwards" }}>
            <img
              src="/img/images.jpeg"
              alt="Book"
              style={styles.bookImage}
            />
          </div>

          {/* Right Content */}
          <div style={{ ...styles.right, animation: "fadeIn 1.2s forwards" }}>
            <p style={styles.badge}>SirAhsanKhan Book Series</p>

            <h1 style={styles.title}>Physical AI & Humanoid Robotics</h1>

            <p style={styles.subtitle}>
              Colearning Agentic AI with Python and TypeScript — 
              <strong> Physical AI & Humanoid Robotics</strong>
            </p>

            <div style={styles.tags}>
              <span style={styles.tag}>🔓 Open Source</span>
              <span style={styles.tag}>🤝 Co-Learning with AI</span>
              <span style={styles.tag}>🎯 Spec-Driven Development</span>
            </div>

            <div style={styles.buttons}>
              <a
                href="https://github.com/SirAhsanKhan/spec-driven-AI-hackathon"
                target="_blank"
                rel="noopener noreferrer"
                style={styles.explore}
              >
                Explore my GitHub 🎓
              </a>

              <Link
                style={styles.primary}
                to="/docs/physical-ai-humanoid-robotics/commercial-viability"
              >
                Start Reading →
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* ================= FOOTER ================= */}
      <footer style={styles.footer}>
        <p>© {new Date().getFullYear()} SirAhsanKhan — All Rights Reserved.</p>
        <p>Built with ❤️ using Docusaurus & AI</p>
      </footer>

      {/* ================= ANIMATIONS ================= */}
      <style>
        {`
          @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
          }

          @keyframes fadeInLeft {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
          }

          @keyframes float {
            0% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0); }
          }
        `}
      </style>
    </>
  );
}

/* ================= INLINE STYLES ================= */
const styles = {
  header: {
    position: "sticky",
    top: 0,
    zIndex: 100,
    backdropFilter: "blur(8px)",
    background: "rgba(0, 0, 0, 0.6)",
    padding: "1rem 2rem",
  },

  navbar: {
    display: "flex",
    justifyContent: "space-between",
    maxWidth: "1400px",
    margin: "auto",
    alignItems: "center",
  },

  logo: {
    fontSize: "1.5rem",
    fontWeight: "700",
    color: "white",
  },

  navLinks: {
    display: "flex",
    gap: "1.5rem",
  },

  navItem: {
    color: "#ccc",
    textDecoration: "none",
    fontSize: "1rem",
  },

  hero: {
    padding: "4rem 2rem",
    background: "#0d0d0d",
    color: "white",
  },

  heroContent: {
    display: "flex",
    gap: "3rem",
    maxWidth: "1400px",
    margin: "auto",
    alignItems: "center",
    justifyContent: "center",
  },

  left: {
    flex: "0 0 330px",
  },

  bookImage: {
    width: "100%",
    borderRadius: "18px",
    boxShadow: "0px 10px 30px rgba(0, 255, 255, 0.25)",
    animation: "float 5s infinite ease-in-out",
  },

  right: {
    maxWidth: "600px",
  },

  badge: {
    opacity: "0.7",
    fontSize: "0.9rem",
    marginBottom: "1rem",
    letterSpacing: "0.08em",
  },

  title: {
    fontSize: "3rem",
    fontWeight: "800",
    marginBottom: "1rem",
  },

  subtitle: {
    fontSize: "1.25rem",
    lineHeight: "1.6",
    marginBottom: "2rem",
  },

  tags: {
    display: "flex",
    gap: "1rem",
    flexWrap: "wrap",
    marginBottom: "2.5rem",
  },

  tag: {
    padding: "0.6rem 1rem",
    background: "#1a1a1a",
    borderRadius: "20px",
  },

  buttons: {
    display: "flex",
    gap: "1rem",
  },

  explore: {
    padding: "0.8rem 1.4rem",
    background: "#222",
    borderRadius: "26px",
    border: "1px solid #444",
    color: "white",
    textDecoration: "none",
  },

  primary: {
    padding: "0.8rem 1.4rem",
    background: "white",
    color: "black",
    borderRadius: "26px",
    fontWeight: "bold",
    textDecoration: "none",
  },

  footer: {
    background: "#0a0a0a",
    color: "#bbb",
    padding: "2rem",
    marginTop: "4rem",
    textAlign: "center",
  },
};
