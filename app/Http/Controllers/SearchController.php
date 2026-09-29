<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class SearchController extends Controller
{
    public function index(Request $request)
    {
        $query = $request->input('q');
        $results = [];
        $error = null;
        $timeTaken = 0;

        if ($query) {
            $startTime = microtime(true);
            try {
                // Kita akan memanggil API Python Flask/FastAPI yang berjalan di port 5000
                $response = Http::timeout(60)->get('http://127.0.0.1:5000/search', [
                    'q' => $query
                ]);

                if ($response->successful()) {
                    $results = $response->json();
                } else {
                    $error = "Terjadi kesalahan pada server pencarian (API Python). Status: " . $response->status();
                }
            } catch (\Exception $e) {
                $error = "Tidak dapat terhubung ke server pencarian (AI Engine). Pastikan backend Python sudah berjalan di http://127.0.0.1:5000. Detail: " . $e->getMessage();
            }
            $timeTaken = round((microtime(true) - $startTime), 3);
        }

        return view('search', compact('results', 'query', 'error', 'timeTaken'));
    }
}
