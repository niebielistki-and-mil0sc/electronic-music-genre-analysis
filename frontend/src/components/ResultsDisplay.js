// src/components/ResultsDisplay.js
import React, { useContext, useState, useEffect } from 'react';
import './css/ResultsDisplay.css';
import AnalysisContext from '../AnalysisContext';
import GenreData from '../GenreData';

const shuffleArray = (array) => {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]]; // Swap elements
  }
  return array;
};

const ResultsDisplay = () => {
  const { results, fileName } = useContext(AnalysisContext);
  const [detailedResults, setDetailedResults] = useState([]);

  useEffect(() => {
    if (results) {
      const genreColors = ['#641eb0', '#4b8e7f', '#1a65bc', '#e93cac', '#c8b029'];
      const shuffledColors = shuffleArray([...genreColors]);

      const transformGenreKey = (genre) =>
        genre.toLowerCase().replace(/ & /g, ' and ').replace(/\s+/g, '_').replace(/[^\w_]/g, '');

      const parsed = Object.entries(results).map(([genre, percentageString], index) => {
        const percentage = parseFloat(percentageString.replace('%', ''));
        const genreKey = transformGenreKey(genre);
        const genreData = GenreData[genreKey] || {};

        return {
          genre,
          percentage,
          color: shuffledColors[index % shuffledColors.length],
          ...genreData,
        };
      }).filter(result => result && result.percentage > 0);

      setDetailedResults(parsed);
    }
  }, [results]);


  return (
    <div className="results-display">
      {fileName && <h2>{`Analysis Results for ${fileName}`}</h2>}
      <div className="results-list">
        {detailedResults.map((result, index) => (
          <div key={index} className="genre-section">
            {/* Genre percentage bar */}
            <div className="genre-bar-container">
              <div className="genre-bar" style={{ width: `${result.percentage}%`, backgroundColor: result.color }}>
                <span className="genre-label">{`${result.genre} ${result.percentage.toFixed(2)}%`}</span>
              </div>
            </div>
            {/* Genre content */}
            <div className="genre-content">
              {/* Image container */}
              <div className="genre-image-container">
                {result.image && <img src={result.image} alt={`${result.genre}`} />}
              </div>
              {/* Description container */}
              <div className="genre-description-container">
                <h3 className="genre-title">{result.genre.toUpperCase()}</h3>
                {result.description && <p className="genre-description">{result.description}</p>}
                {result.readMoreLink && (
                  <a className="genre-read-more" href={result.readMoreLink} target="_blank" rel="noopener noreferrer">
                    Read more
                  </a>
                )}
              </div>
              {/* Artist list container */}
              <div className="genre-artists-container">
                <ul className="artist-list">
                  {result.artists && result.artists.map((artist, artistIndex) => (
                    <li key={artistIndex} className="artist-name">{artist}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResultsDisplay;

