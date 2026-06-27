#!/usr/bin/env node

import {
  copyFileSync,
  lstatSync,
  mkdirSync,
  readdirSync,
  renameSync,
  statSync,
  symlinkSync,
} from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const scriptPath = fileURLToPath(import.meta.url);
const repoRoot = resolve(dirname(scriptPath), "..");
const positionalArgs = process.argv.slice(2).filter((arg) => !arg.startsWith("--"));
const targetArg = positionalArgs[0];
const targetRoot = resolve(targetArg ?? ".");
const force = process.argv.includes("--force");
const dryRun = process.argv.includes("--dry-run");

const timestamp = new Date().toISOString().replace(/[:.]/g, "-");

const entries = [
  { source: "AGENTS.md", target: "AGENTS.md", type: "file" },
  { source: "CLAUDE.md", target: "CLAUDE.md", type: "file" },
  { source: ".claude/settings.json", target: ".claude/settings.json", type: "file" },
  { source: ".agents/skills", target: ".agents/skills", type: "directory" },
  { target: ".claude/skills", type: "symlink", linkTarget: "../.agents/skills" },
];

const copied = [];
const linked = [];
const skipped = [];
const backedUp = [];

const pathExists = (targetPath) => {
  try {
    lstatSync(targetPath);

    return true;
  } catch {
    return false;
  }
};

const ensureParent = (filePath) => {
  mkdirSync(dirname(filePath), { recursive: true });
};

const backupPathFor = (targetPath) => `${targetPath}.bak-${timestamp}`;

const backupExisting = (targetPath) => {
  const backupPath = backupPathFor(targetPath);

  if (!dryRun) {
    renameSync(targetPath, backupPath);
  }

  backedUp.push(relative(targetRoot, backupPath));
};

const copyFileWithPolicy = (sourcePath, targetPath) => {
  const relTarget = relative(targetRoot, targetPath);

  if (pathExists(targetPath)) {
    if (!force) {
      skipped.push(relTarget);

      return;
    }

    backupExisting(targetPath);
  }

  if (!dryRun) {
    ensureParent(targetPath);
    copyFileSync(sourcePath, targetPath);
  }

  copied.push(relTarget);
};

const createSymlinkWithPolicy = (targetPath, linkTarget) => {
  const relTarget = relative(targetRoot, targetPath);

  if (pathExists(targetPath)) {
    if (!force) {
      skipped.push(relTarget);

      return;
    }

    backupExisting(targetPath);
  }

  if (!dryRun) {
    ensureParent(targetPath);
    symlinkSync(linkTarget, targetPath, "dir");
  }

  linked.push(`${relTarget} -> ${linkTarget}`);
};

const copyDirectoryWithPolicy = (sourceDir, targetDir) => {
  for (const entry of readdirSync(sourceDir)) {
    const sourcePath = join(sourceDir, entry);
    const targetPath = join(targetDir, entry);
    const stats = statSync(sourcePath);

    if (stats.isDirectory()) {
      copyDirectoryWithPolicy(sourcePath, targetPath);
      continue;
    }

    copyFileWithPolicy(sourcePath, targetPath);
  }
};

for (const entry of entries) {
  const targetPath = join(targetRoot, entry.target);

  if (entry.type === "symlink") {
    createSymlinkWithPolicy(targetPath, entry.linkTarget);
    continue;
  }

  const sourcePath = join(repoRoot, entry.source);

  if (entry.type === "file") {
    copyFileWithPolicy(sourcePath, targetPath);
    continue;
  }

  if (!dryRun) {
    mkdirSync(targetPath, { recursive: true });
  }

  copyDirectoryWithPolicy(sourcePath, targetPath);
}

const mode = dryRun ? "Dry run" : "Applied";

console.log(`${mode} agent kit to ${targetRoot}`);

if (copied.length > 0) {
  console.log("\nCopied:");
  copied.forEach((item) => console.log(`- ${item}`));
}

if (linked.length > 0) {
  console.log("\nLinked:");
  linked.forEach((item) => console.log(`- ${item}`));
}

if (backedUp.length > 0) {
  console.log("\nBacked up:");
  backedUp.forEach((item) => console.log(`- ${item}`));
}

if (skipped.length > 0) {
  console.log("\nSkipped existing files:");
  skipped.forEach((item) => console.log(`- ${item}`));
  console.log("\nRerun with --force to replace skipped files after review.");
}
