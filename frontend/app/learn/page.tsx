'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowLeft, BookOpen } from 'lucide-react';

export default function LearnPage() {
  const [radicals, setRadicals] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // This would fetch from your API
    // For now, showing placeholder data
    setLoading(false);
    setRadicals([
      { id: '1', character: '人', meaning: 'person', stroke_count: 2 },
      { id: '2', character: '口', meaning: 'mouth', stroke_count: 3 },
      { id: '3', character: '手', meaning: 'hand', stroke_count: 4 },
      { id: '4', character: '心', meaning: 'heart', stroke_count: 4 },
      { id: '5', character: '水', meaning: 'water', stroke_count: 4 },
      { id: '6', character: '木', meaning: 'tree/wood', stroke_count: 4 },
      { id: '7', character: '火', meaning: 'fire', stroke_count: 4 },
      { id: '8', character: '土', meaning: 'earth', stroke_count: 3 },
    ]);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/">
                <Button variant="ghost" size="sm">
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Back
                </Button>
              </Link>
              <h1 className="text-2xl font-bold">Radical Library</h1>
            </div>
            <Link href="/dashboard">
              <Button variant="outline">Go to Dashboard</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-2">Learn Chinese Radicals</h2>
          <p className="text-gray-600">
            Radicals are the building blocks of Chinese characters. Master these to understand how characters are formed.
          </p>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Loading radicals...</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {radicals.map((radical) => (
              <Card key={radical.id} className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader className="text-center">
                  <div className="text-6xl mb-2">{radical.character}</div>
                  <CardTitle className="text-lg">{radical.meaning}</CardTitle>
                </CardHeader>
                <CardContent className="text-center">
                  <p className="text-sm text-gray-600">
                    {radical.stroke_count} stroke{radical.stroke_count !== 1 ? 's' : ''}
                  </p>
                  <Button variant="outline" size="sm" className="mt-4 w-full">
                    <BookOpen className="w-4 h-4 mr-2" />
                    Learn More
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {!loading && radicals.length === 0 && (
          <div className="text-center py-12">
            <BookOpen className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <h3 className="text-xl font-semibold mb-2">No radicals available yet</h3>
            <p className="text-gray-600 mb-4">
              The database needs to be seeded with learning content.
            </p>
            <p className="text-sm text-gray-500">
              Run the seed script: <code className="bg-gray-100 px-2 py-1 rounded">python backend/seed_data.py</code>
            </p>
          </div>
        )}
      </main>
    </div>
  );
}
