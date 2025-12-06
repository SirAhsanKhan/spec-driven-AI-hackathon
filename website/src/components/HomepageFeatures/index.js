import React from "react";
import Link from "@docusaurus/Link";
import styles from "./styles.module.css";

export default function Hero() {
  return (
    <section className={styles.hero}>
      <div className={styles.heroContent}>
        <div className={styles.left}>
          <img
            src="/img/ai-native-book.png"
            alt="AI Native Software Development Book"
            className={styles.bookImage}
          />
        </div>

        <div className={styles.right}>
          <p className={styles.badge}>PANAVERSITY AI-NATIVE BOOK SERIES</p>

          <h1 className={styles.title}>AI Native Software Development</h1>

          <p className={styles.subtitle}>
            Colearning Agentic AI with Python and TypeScript — 
            <strong> Spec Driven Reusable Intelligence</strong>
          </p>

          <div className={styles.tags}>
            <span>🔓 Open Source</span>
            <span>🤝 Co-Learning with AI</span>
            <span>🎯 Spec-Driven Development</span>
          </div>

          <div className={styles.buttons}>
            <Link className={styles.explore} to="/explore">
              Explore Panaversity 🎓
            </Link>

            <Link className={styles.primary} to="/docs/intro">
              Start Reading →
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
