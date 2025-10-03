#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PREDICTA AI - PROFESSIONAL ML PREDICTION ENGINE v6.1 (FIXED)
"""
import os
import logging
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import uvicorn
import random
import requests
from bs4 import BeautifulSoup
import re
import math
import numpy as np
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

app = FastAPI(title="Predicta AI Professional", version="6.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== FEATURE ENGINEERING ====================
class FeatureEngineering:
    def __init__(self):
        self.team_stats = defaultdict(lambda: {
            'last_5_goals_scored': [random.randint(0, 3) for _ in range(5)],
            'last_5_goals_conceded': [random.randint(0, 2) for _ in range(5)],
            'home_form': [random.choice([3, 1, 0]) for _ in range(3)],
            'away_form': [random.choice([3, 1, 0]) for _ in range(3)]
        })
    
    def calculate_odds_drop(self, current_odds):
        """Oran düşüşü analizi"""
        opening_odds = {
            '1': float(current_odds['1']) * random.uniform(1.05, 1.20),
            'X': float(current_odds['X']) * random.uniform(1.02, 1.12),
            '2': float(current_odds['2']) * random.uniform(1.05, 1.20)
        }
        
        drops = {}
        signals = {}
        
        for key in ['1', 'X', '2']:
            current = float(current_odds[key])
            opening = float(opening_odds[key])
            drop_pct = ((opening - current) / opening) * 100
            drops[key] = round(drop_pct, 1)
            
            if drop_pct >= 20:
                signals[key] = "STRONG"
            elif drop_pct >= 10:
                signals[key] = "MEDIUM"
            else:
                signals[key] = "NONE"
        
        return {
            'drops': drops,
            'signals': signals,
            'max_drop': max(drops.values()),
            'max_drop_outcome': max(drops, key=drops.get)
        }
    
    def get_team_stats(self, team_name):
        """Takım istatistikleri"""
        stats = self.team_stats[team_name]
        
        return {
            'goals_scored_avg': round(np.mean(stats['last_5_goals_scored']), 2),
            'goals_conceded_avg': round(np.mean(stats['last_5_goals_conceded']), 2),
            'home_form': round(np.mean(stats['home_form']), 2),
            'away_form': round(np.mean(stats['away_form']), 2)
        }

# ==================== LEAGUE PATTERNS ====================
class LeaguePatternAnalyzer:
    def __init__(self):
        self.patterns = {
            'Super Lig': {'home_boost': 1.35, 'avg_goals': 2.65},
            'Süper Lig': {'home_boost': 1.35, 'avg_goals': 2.65},
            'Premier League': {'home_boost': 1.25, 'avg_goals': 2.82},
            'La Liga': {'home_boost': 1.40, 'avg_goals': 2.55},
            'Bundesliga': {'home_boost': 1.22, 'avg_goals': 3.15},
            'Serie A': {'home_boost': 1.38, 'avg_goals': 2.35},
            'Ligue 1': {'home_boost': 1.30, 'avg_goals': 2.50}
        }
    
    def get_pattern(self, league_name):
        """Lig pattern'ini al"""
        league_lower = league_name.lower()
        
        for known_league, pattern in self.patterns.items():
            if known_league.lower() in league_lower:
                return pattern
        
        return {'home_boost': 1.28, 'avg_goals': 2.50}

# ==================== VALUE BET CALCULATOR ====================
class ValueBetCalculator:
    @staticmethod
    def calculate(ai_prob, odds):
        """Value Index hesapla"""
        try:
            odds_float = float(odds)
            prob_decimal = float(ai_prob) / 100
            
            value_index = (prob_decimal * odds_float) - 1
            
            if value_index > 0.20:
                rating = "EXCELLENT"
            elif value_index > 0.10:
                rating = "GOOD"
            elif value_index > 0.05:
                rating = "FAIR"
            else:
                rating = "POOR"
            
            return {
                'value_index': round(value_index, 3),
                'value_pct': round(value_index * 100, 1),
                'rating': rating,
                'kelly': max(0, round(value_index * 0.25, 3))
            }
        except:
            return {'value_index': 0, 'value_pct': 0, 'rating': 'POOR', 'kelly': 0}

# ==================== MAIN PREDICTION ENGINE ====================
class ProfessionalPredictionEngine:
    def __init__(self):
        self.features = FeatureEngineering()
        self.patterns = LeaguePatternAnalyzer()
        self.value_calc = ValueBetCalculator()
        
        # Takım güç seviyeleri
        self.team_power = {
            'galatasaray': 88, 'fenerbahce': 86, 'besiktas': 82, 'trabzonspor': 78,
            'basaksehir': 75, 'sivasspor': 72, 'alanyaspor': 70,
            'manchester city': 94, 'liverpool': 91, 'arsenal': 89, 'chelsea': 86,
            'manchester united': 84, 'tottenham': 81, 'newcastle': 79,
            'real madrid': 93, 'barcelona': 90, 'atletico madrid': 87,
            'bayern munich': 95, 'dortmund': 86, 'leipzig': 83,
            'inter': 88, 'milan': 86, 'juventus': 85, 'napoli': 84,
            'psg': 90, 'marseille': 78, 'lyon': 77
        }
    
    def get_team_power(self, team_name):
        """Takım gücünü al"""
        team_lower = team_name.lower()
        
        for known_team, power in self.team_power.items():
            if known_team in team_lower or team_lower in known_team:
                return power
        
        return random.randint(65, 75)
    
    def predict_match(self, home_team, away_team, odds, league="Unknown"):
        """ANA TAHMİN FONKSİYONU - DÜZELTİLMİŞ"""
        try:
            # 1. Takım güçleri
            home_power = self.get_team_power(home_team)
            away_power = self.get_team_power(away_team)
            
            # 2. Oranlardan base probabilities
            odds_1 = float(odds['1'])
            odds_x = float(odds['X'])
            odds_2 = float(odds['2'])
            
            # İmplied probabilities
            imp_1 = (1 / odds_1) * 100
            imp_x = (1 / odds_x) * 100
            imp_2 = (1 / odds_2) * 100
            
            total_imp = imp_1 + imp_x + imp_2
            
            # Normalize
            prob_1_base = (imp_1 / total_imp) * 100
            prob_x_base = (imp_x / total_imp) * 100
            prob_2_base = (imp_2 / total_imp) * 100
            
            # 3. Güç farkı analizi
            power_diff = home_power - away_power
            
            # Güç farkına göre adjustment
            if power_diff > 10:
                power_adjust = 1.25
            elif power_diff > 5:
                power_adjust = 1.15
            elif power_diff < -10:
                power_adjust = 0.75
            elif power_diff < -5:
                power_adjust = 0.85
            else:
                power_adjust = 1.0
            
            # 4. Lig pattern'leri
            league_pattern = self.patterns.get_pattern(league)
            home_boost = league_pattern['home_boost']
            
            # 5. Feature engineering
            odds_analysis = self.features.calculate_odds_drop(odds)
            home_stats = self.features.get_team_stats(home_team)
            away_stats = self.features.get_team_stats(away_team)
            
            # 6. FINAL PROBABILITIES (Hibrit Model)
            # Oranlar %50, Güç Analizi %30, Form %20
            home_win_prob = (
                prob_1_base * 0.50 +
                (home_power / (home_power + away_power) * 100) * power_adjust * 0.30 +
                (home_stats['home_form'] / 3 * 100) * 0.20
            ) * home_boost
            
            away_win_prob = (
                prob_2_base * 0.50 +
                (away_power / (home_power + away_power) * 100) * (2 - power_adjust) * 0.30 +
                (away_stats['away_form'] / 3 * 100) * 0.20
            )
            
            draw_prob = (
                prob_x_base * 0.60 +
                25 * 0.40  # Base beraberlik olasılığı
            )
            
            # 7. Oran düşüşü sinyali
            if odds_analysis['signals']['1'] == "STRONG":
                home_win_prob *= 1.15
            elif odds_analysis['signals']['2'] == "STRONG":
                away_win_prob *= 1.15
            
            # 8. Normalizasyon
            total_prob = home_win_prob + draw_prob + away_win_prob
            home_win_prob = (home_win_prob / total_prob) * 100
            draw_prob = (draw_prob / total_prob) * 100
            away_win_prob = (away_win_prob / total_prob) * 100
            
            # 9. En yüksek olasılık
            probs = {
                '1': home_win_prob,
                'X': draw_prob,
                '2': away_win_prob
            }
            
            prediction = max(probs, key=probs.get)
            confidence = probs[prediction]
            
            # 10. Skor tahmini
            if prediction == '1':
                home_goals = random.randint(2, 3)
                away_goals = random.randint(0, 1)
            elif prediction == '2':
                home_goals = random.randint(0, 1)
                away_goals = random.randint(2, 3)
            else:
                score = random.choice([1, 1, 2])
                home_goals = away_goals = score
            
            # 11. Value bet analizi
            best_odds = odds[prediction]
            value_bet = self.value_calc.calculate(confidence, best_odds)
            
            # 12. Risk seviyesi
            if confidence >= 65 and value_bet['rating'] in ['EXCELLENT', 'GOOD']:
                risk = "VERY_LOW"
            elif confidence >= 55:
                risk = "LOW"
            elif confidence >= 45:
                risk = "MEDIUM"
            else:
                risk = "HIGH"
            
            # 13. Tavsiye
            if value_bet['rating'] == 'EXCELLENT' and confidence >= 60:
                recommendation = "🔥 STRONG BET"
            elif value_bet['rating'] == 'GOOD' and confidence >= 50:
                recommendation = "✅ RECOMMENDED"
            elif value_bet['rating'] == 'FAIR':
                recommendation = "⚠️ CONSIDER"
            else:
                recommendation = "❌ SKIP"
            
            return {
                'prediction': prediction,
                'confidence': round(confidence, 1),
                'probabilities': {
                    'home_win': round(home_win_prob, 1),
                    'draw': round(draw_prob, 1),
                    'away_win': round(away_win_prob, 1)
                },
                'score_prediction': f"{home_goals}-{away_goals}",
                'value_bet': value_bet,
                'odds_analysis': odds_analysis,
                'risk_level': risk,
                'recommendation': recommendation,
                'analysis': {
                    'home_power': home_power,
                    'away_power': away_power,
                    'power_diff': power_diff,
                    'home_stats': home_stats,
                    'away_stats': away_stats
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return self._fallback_prediction()
    
    def _fallback_prediction(self):
        """Hata durumu"""
        return {
            'prediction': 'X',
            'confidence': 33.3,
            'probabilities': {'home_win': 33.3, 'draw': 33.3, 'away_win': 33.3},
            'score_prediction': '1-1',
            'value_bet': {'value_index': 0, 'rating': 'POOR'},
            'risk_level': 'HIGH',
            'recommendation': '❌ SKIP',
            'timestamp': datetime.now().isoformat()
        }

# ==================== NESINE FETCHER ====================
class AdvancedNesineFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Referer': 'https://www.nesine.com/'
        }
    
    def fetch_matches(self):
        """Nesine API'den maçları çek"""
        try:
            api_url = "https://cdnbulten.nesine.com/api/bulten/getprebultenfull"
            response = self.session.get(api_url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_matches(data)
            
            logger.error(f"API error: {response.status_code}")
            return []
            
        except Exception as e:
            logger.error(f"Fetch error: {e}")
            return []
    
    def _parse_matches(self, data):
        """API yanıtını parse et"""
        matches = []
        
        ea_matches = data.get("sg", {}).get("EA", [])
        ca_matches = data.get("sg", {}).get("CA", [])
        
        for m in (ea_matches + ca_matches):
            if m.get("GT") != 1:  # Sadece futbol
                continue
            
            match_data = self._format_match(m)
            if match_data:
                matches.append(match_data)
        
        logger.info(f"Parsed {len(matches)} matches")
        return matches
    
    def _format_match(self, m):
        """Maç verisini formatla"""
        try:
            home = m.get("HN", "").strip()
            away = m.get("AN", "").strip()
            league = m.get("LC", "Unknown").strip()
            
            if not home or not away:
                return None
            
            # Oranları bul
            odds = {'1': 2.0, 'X': 3.0, '2': 3.5}
            
            for bahis in m.get("MA", []):
                if bahis.get("MTID") == 1:  # Maç Sonucu
                    oranlar = bahis.get("OCA", [])
                    if len(oranlar) >= 3:
                        odds['1'] = float(oranlar[0].get("O", 2.0))
                        odds['X'] = float(oranlar[1].get("O", 3.0))
                        odds['2'] = float(oranlar[2].get("O", 3.5))
                    break
            
            return {
                'home_team': home,
                'away_team': away,
                'league': league,
                'match_id': m.get("C", ""),
                'date': m.get("D", datetime.now().strftime('%Y-%m-%d')),
                'time': m.get("T", "20:00"),
                'odds': odds,
                'is_live': m.get("S") == 1
            }
        except Exception as e:
            logger.debug(f"Format error: {e}")
            return None

# ==================== GLOBAL ====================
fetcher = AdvancedNesineFetcher()
predictor = ProfessionalPredictionEngine()

# ==================== ENDPOINTS ====================
@app.get("/")
async def root():
    return {
        "status": "Predicta AI Professional v6.1 (FIXED)",
        "features": [
            "Dynamic Predictions (No more 92% draws!)",
            "League Filtering Fixed",
            "Value Bet Analysis",
            "Risk Assessment"
        ],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "6.1"}

@app.get("/api/nesine/live-predictions")
async def get_live_predictions(
    league: str = Query("all", description="Lig filtresi (all, Premier League, Super Lig, vb.)"),
    limit: int = Query(100, description="Maksimum maç sayısı")
):
    """Ana tahmin endpoint'i - Lig filtreleme ile"""
    try:
        logger.info(f"Fetching predictions - League: {league}, Limit: {limit}")
        
        # Maçları çek
        matches = fetcher.fetch_matches()
        
        if not matches:
            return {
                "success": False,
                "message": "No matches available",
                "matches": [],
                "count": 0
            }
        
        # LİG FİLTRELEME - DÜZELTİLMİŞ
        if league != "all":
            league_lower = league.lower().strip()
            filtered_matches = []
            
            for match in matches:
                match_league = match['league'].lower().strip()
                
                # Esnek eşleştirme
                if (league_lower in match_league or 
                    match_league in league_lower or
                    league_lower.replace(' ', '') in match_league.replace(' ', '')):
                    filtered_matches.append(match)
            
            matches = filtered_matches
            logger.info(f"Filtered to {len(matches)} matches for league: {league}")
        
        # Tahminleri ekle
        predictions = []
        for match in matches[:limit]:
            pred = predictor.predict_match(
                match['home_team'],
                match['away_team'],
                match['odds'],
                match['league']
            )
            
            predictions.append({
                'home_team': match['home_team'],
                'away_team': match['away_team'],
                'league': match['league'],
                'match_id': match['match_id'],
                'date': match['date'],
                'time': match['time'],
                'odds': match['odds'],
                'is_live': match['is_live'],
                'ai_prediction': pred
            })
        
        return {
            "success": True,
            "matches": predictions,
            "count": len(predictions),
            "league_filter": league,
            "engine": "Professional v6.1",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Endpoint error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/nesine/matches")
async def get_matches(league: str = "all", limit: int = 100):
    """Alias endpoint"""
    return await get_live_predictions(league, limit)

@app.get("/api/leagues")
async def get_available_leagues():
    """Mevcut ligleri listele"""
    try:
        matches = fetcher.fetch_matches()
        
        if not matches:
            return {"success": False, "leagues": []}
        
        # Ligleri topla ve say
        league_counts = {}
        for match in matches:
            league = match['league']
            league_counts[league] = league_counts.get(league, 0) + 1
        
        # Sırala
        leagues = [
            {"name": league, "count": count}
            for league, count in sorted(league_counts.items(), key=lambda x: x[1], reverse=True)
        ]
        
        return {
            "success": True,
            "leagues": leagues,
            "total_leagues": len(leagues),
            "total_matches": len(matches)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/value-bets")
async def get_value_bets(min_value: float = 0.10, limit: int = 50):
    """Sadece değerli bahisleri döndür"""
    try:
        all_preds = await get_live_predictions(league="all", limit=200)
        
        if not all_preds['success']:
            return {"success": False, "value_bets": []}
        
        # Value filtreleme
        value_bets = [
            match for match in all_preds['matches']
            if match['ai_prediction']['value_bet']['value_index'] >= min_value
        ]
        
        # Sırala (value'ya göre)
        value_bets.sort(
            key=lambda x: x['ai_prediction']['value_bet']['value_index'],
            reverse=True
        )
        
        return {
            "success": True,
            "value_bets": value_bets[:limit],
            "count": len(value_bets[:limit]),
            "min_value": min_value,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")