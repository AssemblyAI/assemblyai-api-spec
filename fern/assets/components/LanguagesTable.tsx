"use client";
import * as React from "react";

interface Language {
  name: string;
  code: string;
}

interface LanguageTableProps {
  languages: Language[];
  columns?: number;
}

export function LanguageTable({ languages, columns = 3 }: LanguageTableProps) {
  return (
    <div
      className="grid gap-2"
      style={{ gridTemplateColumns: `repeat(${columns}, 1fr)` }}
    >
      {languages.map((language) => (
        <div key={language.code} className="flex justify-between items-center">
          <span>{language.name}</span>
          <code className="text-sm bg-gray-100 px-2 py-1 rounded">
            {language.code}
          </code>
        </div>
      ))}
    </div>
  );
}
