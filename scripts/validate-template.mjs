#!/usr/bin/env node

import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const scriptPath = fileURLToPath(import.meta.url);
const repoRoot = resolve(dirname(scriptPath), "..");

const requiredFiles = [
  "README.md",
  "AGENTS.md",
  "package.json",
  "scripts/apply-agent-kit.mjs",
  "scripts/validate-template.mjs",
  "templates/PROJECT_PROFILE.md",
  ".agents/skills/build-fix/SKILL.md",
  ".agents/skills/update-expo-deps/SKILL.md",
  ".agents/skills/routing-patterns/SKILL.md",
  ".agents/skills/zustand-patterns/SKILL.md",
];

const forbiddenPatterns = [
  { name: "absolute local project path", pattern: /\/Users\/[^/\s]+\/Github\/[A-Za-z0-9._-]+/ },
  { name: "GitHub token", pattern: /gh[oprsu]_[A-Za-z0-9_]+/ },
  { name: "OpenAI API key", pattern: /sk-[A-Za-z0-9_-]{20,}/ },
  { name: "Supabase JWT-like service key", pattern: /eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/ },
];

const errors = [];

for (const file of requiredFiles) {
  if (!existsSync(join(repoRoot, file))) {
    errors.push(`missing required file: ${file}`);
  }
}

const collectMarkdownFiles = (dir) => {
  const output = [];

  for (const entry of readdirSync(dir)) {
    const fullPath = join(dir, entry);
    const stats = statSync(fullPath);

    if (stats.isDirectory()) {
      output.push(...collectMarkdownFiles(fullPath));
      continue;
    }

    if (entry.endsWith(".md")) {
      output.push(fullPath);
    }
  }

  return output;
};

for (const filePath of collectMarkdownFiles(repoRoot)) {
  const text = readFileSync(filePath, "utf8");

  for (const { name, pattern } of forbiddenPatterns) {
    if (pattern.test(text)) {
      errors.push(`${name} found in ${filePath}`);
    }
  }
}

if (errors.length > 0) {
  console.error("Template validation failed:");
  errors.forEach((error) => console.error(`- ${error}`));
  process.exit(1);
}

console.log("Template validation passed.");
