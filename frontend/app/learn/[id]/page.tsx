'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowLeft, BookOpen } from 'lucide-react';
import { getRadicalById } from '@/lib/firestore-service';
import { Radical } from '@/lib/types';

export default function RadicalDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [radical, setRadical] = useState<Radical | null>(null);
  const [examples, setExamples] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRadical = async () => {
      setLoading(true);
      const data = await getRadicalById(params.id as string) as Radical | null;
      
      if (data) {
        setRadical(data);
        setExamples(data.examples || []);
      }
      
      setLoading(false);
    };
    
    if (params.id) {
      fetchRadical();
    }
  }, [params.id]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!radical) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4">Radical not found</h2>
          <Link href="/learn">
            <Button>Back to Radicals</Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link href="/learn">
              <Button variant="ghost" size="sm">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Radicals
              </Button>
            </Link>
            <Link href="/dashboard">
              <Button variant="outline">Dashboard</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Radical Display */}
        <Card className="mb-8">
          <CardContent className="p-8">
            <div className="text-center">
              <div className="text-9xl mb-4">{radical.character}</div>
              <h1 className="text-4xl font-bold mb-2">{radical.meaning}</h1>
              <p className="text-xl text-gray-600">
                {radical.stroke_count} stroke{radical.stroke_count !== 1 ? 's' : ''}
              </p>
            </div>
          </CardContent>
        </Card>

        {/* About Section */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="text-2xl">About This Radical</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-700 leading-relaxed">
              The radical <span className="text-2xl font-bold">{radical.character}</span> ({radical.meaning}) 
              is a fundamental building block in Chinese characters. It appears in many characters and 
              often provides a clue to the meaning or pronunciation of the complete character.
            </p>
          </CardContent>
        </Card>

        {/* Examples Section */}
        {examples.length > 0 && (
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="text-2xl">Example Characters</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 mb-4">
                Here are some characters that include the {radical.meaning} radical:
              </p>
              <div className="grid gap-4">
                {examples.map((example, index) => (
                  <div 
                    key={index} 
                    className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                  >
                    <span className="text-4xl">{example.split(' ')[0]}</span>
                    <span className="text-gray-700">{example.split(' ').slice(1).join(' ')}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Learning Tips */}
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">Learning Tips</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-3 text-gray-700">
              <li className="flex items-start gap-2">
                <span className="text-blue-600 font-bold">•</span>
                <span>Practice writing this radical multiple times to memorize the stroke order</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600 font-bold">•</span>
                <span>Look for this radical in compound characters to help remember meanings</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600 font-bold">•</span>
                <span>Use flashcards and spaced repetition to reinforce your memory</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600 font-bold">•</span>
                <span>Try to create associations between the radical's shape and its meaning</span>
              </li>
            </ul>
          </CardContent>
        </Card>

        {/* Action Buttons */}
        <div className="flex gap-4 mt-8 justify-center">
          <Link href="/learn">
            <Button variant="outline" size="lg">
              <BookOpen className="w-5 h-5 mr-2" />
              Browse More Radicals
            </Button>
          </Link>
          <Link href="/dashboard">
            <Button size="lg">
              Start Practicing
            </Button>
          </Link>
        </div>
      </main>
    </div>
  );
}
