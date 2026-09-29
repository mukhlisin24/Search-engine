<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BeritaSearch - Dense Retrieval Search Engine</title>
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    },
                    colors: {
                        primary: '#21409a', // DetikNews Blue
                        secondary: '#e31b23', // DetikNews Red
                        accent: '#fca311', // DetikNews Yellow
                    }
                }
            }
        }
    </script>
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #f3f4f6; }
        .glass {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        .search-input:focus { outline: none; box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.3); }
        .hover-card { transition: all 0.2s ease; }
        .hover-card:hover .title-link { color: #e31b23; } /* Berubah merah saat dihover ala detik */
        .score-badge {
            background: #f1f5f9;
            color: #475569;
            font-weight: 600;
            border: 1px solid #cbd5e1;
        }
    </style>
</head>
<body class="min-h-screen text-gray-800">

    <!-- Header / Navbar -->
    <nav class="bg-primary text-white shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <div class="flex items-center gap-3">
                    <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9.5a2.5 2.5 0 00-2.5-2.5H15M9 11l3 3m0 0l3-3m-3 3V8"></path></svg>
                    <span class="font-bold text-2xl tracking-tight italic">detik<span class="text-accent">News</span></span>
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero / Search Section -->
    <div class="bg-white border-b border-gray-200">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div class="text-center mb-8">
                <h1 class="text-4xl font-bold text-gray-800 mb-3">Temukan Informasi Berita Lebih Akurat!</h1>
                <p class="text-gray-600">Dengan informasi akurat dan terpercaya sesuai kebutuhan anda.</p>
            </div>
            <form action="{{ route('search') }}" method="GET" class="w-full relative flex items-center">
                <input type="text" name="q" value="{{ $query ?? '' }}" placeholder="Cari Berita, Tokoh, atau Peristiwa..." required
                    class="block w-full px-4 py-3 border border-gray-300 rounded-l-md text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary">
                <button type="submit" class="bg-primary hover:bg-blue-800 text-white font-bold py-3 px-6 rounded-r-md transition-colors flex items-center gap-2 border border-primary">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                    Cari
                </button>
            </form>
        </div>
    </div>

    <!-- Search Results Section -->
    <main class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        @if(isset($error))
        <div class="bg-red-50 border-l-4 border-red-500 p-4 mb-8 rounded-r-lg shadow-sm">
            <div class="flex">
                <div class="flex-shrink-0">
                    <svg class="h-5 w-5 text-red-500" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" /></svg>
                </div>
                <div class="ml-3">
                    <h3 class="text-sm font-medium text-red-800">Gagal melakukan pencarian</h3>
                    <p class="text-sm text-red-700 mt-1">{{ $error }}</p>
                </div>
            </div>
        </div>
        @endif

        @if($query && !isset($error))
            <div class="mb-6 flex items-center justify-between border-b border-gray-200 pb-4">
                <h2 class="text-xl text-gray-700 font-medium">Hasil pencarian untuk: <span class="font-bold text-gray-900">"{{ $query }}"</span></h2>
                <div class="text-sm text-gray-500 flex items-center gap-1">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    Waktu: {{ $timeTaken }} detik
                </div>
            </div>

            @if(count($results) > 0)
                <div class="space-y-0 divide-y divide-gray-200 bg-white border border-gray-200">
                    @foreach($results as $item)
                        <div class="p-4 hover-card flex flex-col md:flex-row gap-4 bg-white">
                            @if(!empty($item['main_image']))
                            <div class="md:w-1/4 h-32 relative overflow-hidden flex-shrink-0 bg-gray-100">
                                <img src="{{ $item['main_image'] }}" alt="Thumbnail" class="w-full h-full object-cover">
                            </div>
                            @endif
                            
                            <div class="md:w-3/4 flex flex-col justify-between">
                                <div>
                                    <div class="flex items-center gap-2 mb-1">
                                        @if(isset($item['tag']) && $item['tag'] != '[]')
                                            @php
                                                $tagsStr = str_replace(['[', ']', "'"], '', $item['tag']);
                                                $tags = explode(', ', $tagsStr);
                                            @endphp
                                            <span class="text-secondary font-bold text-xs uppercase">{{ $tags[0] ?? 'BERITA' }}</span>
                                        @endif
                                        <span class="text-gray-400 text-xs flex items-center gap-1 before:content-['•'] before:mr-1">
                                            {{ isset($item['publish_date']) ? date('l, d M Y H:i', strtotime($item['publish_date'])) : '-' }} WIB
                                        </span>
                                    </div>

                                    @php
                                        $cleanUrl = str_replace(['\\/', '\/'], '/', $item['url'] ?? '#');
                                    @endphp
                                    <a href="{{ $cleanUrl }}" target="_blank" class="title-link text-xl font-bold text-gray-900 mb-2 block leading-snug">
                                        {{ $item['title'] ?? 'Tanpa Judul' }}
                                    </a>
                                    
                                    <p class="text-gray-600 text-sm line-clamp-2 leading-relaxed">
                                        {{ Str::limit($item['article_text'] ?? '', 180) }}
                                    </p>
                                </div>
                                
                                <div class="mt-3 flex items-center justify-between">
                                    <span class="text-xs font-semibold text-gray-500 uppercase">{{ $item['author'] ?? 'Redaksi' }}</span>
                                    
                                    <!-- Similarity Score Badge -->
                                    <div class="flex-shrink-0 score-badge px-2 py-0.5 rounded text-[10px] uppercase tracking-wider flex items-center gap-1" title="Similarity Score">
                                        <svg class="w-3 h-3 text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                                        Relevansi: {{ number_format($item['score'] ?? 0, 4) }}
                                    </div>
                                </div>
                            </div>
                        </div>
                    @endforeach
                </div>
            @else
                <div class="text-center py-16 bg-white rounded-2xl shadow-sm border border-gray-100">
                    <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    <h3 class="text-lg font-medium text-gray-900 mb-1">Berita Tidak Ditemukan</h3>
                    <p class="text-gray-500">Kami tidak menemukan artikel yang cocok dengan kata kunci tersebut. Coba kata kunci lain.</p>
                </div>
            @endif
        @elseif(!$query)
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 opacity-60">
                <!-- Skeleton Loading / Placeholder State -->
                @for($i=0; $i<3; $i++)
                <div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
                    <div class="w-full h-32 bg-gray-200 rounded-lg mb-4 animate-pulse"></div>
                    <div class="h-4 bg-gray-200 rounded w-3/4 mb-3 animate-pulse"></div>
                    <div class="h-3 bg-gray-200 rounded w-full mb-2 animate-pulse"></div>
                    <div class="h-3 bg-gray-200 rounded w-5/6 animate-pulse"></div>
                </div>
                @endfor
            </div>
        @endif
        
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200 mt-auto py-8">
        <div class="max-w-5xl mx-auto px-4 text-center">
            <p class="text-gray-500 text-sm">
                Project Akhir Mata Kuliah Temu Kembali Informasi (UAS)
            </p>
            <p class="text-gray-400 text-xs mt-2">
                Dibuat oleh Irwan Dwi Mukhlisin
            </p>
        </div>
    </footer>

</body>
</html>
