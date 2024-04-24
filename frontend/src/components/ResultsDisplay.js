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

// Separate the first sentence and the rest of the description
const splitDescription = (description) => {
  const firstPeriodIndex = description.indexOf('. ');
  if (firstPeriodIndex !== -1) {
    const firstSentence = description.slice(0, firstPeriodIndex + 1);
    const restOfDescription = description.slice(firstPeriodIndex + 2);
    return { firstSentence, restOfDescription: truncateDescription(restOfDescription) };
  }
  return { firstSentence: description, restOfDescription: '' };
};

const truncateDescription = (description) => {
  const maxLength = 1000; // This can be adjusted as needed
  if (description.length > maxLength) {
    const truncated = description.slice(0, maxLength);
    return truncated.slice(0, truncated.lastIndexOf('.')) + '.';
  }
  return description;
};

const createWikiLink = (artistName) => {
  return `https://en.wikipedia.org/wiki/${artistName.split(' ').join('_')}`;
};

const ResultsDisplay = () => {
  const { results, fileName } = useContext(AnalysisContext);
  const [detailedResults, setDetailedResults] = useState([]);
  const [animate, setAnimate] = useState(false);

  useEffect(() => {
    if (results) {
      const genreColors = ['#641eb0', '#4b8e7f', '#1a65bc', '#e93cac', '#c8b029'];
      const shuffledColors = shuffleArray([...genreColors]);

      const transformGenreKey = (genre) =>
        genre.toLowerCase().replace(/ & /g, ' and ').replace(/\s+/g, '_').replace(/[^\w_]/g, '');


      let parsed = Object.entries(results).map(([genre, percentageString], index) => {
        const percentage = parseFloat(percentageString.replace('%', ''));
        const genreKey = transformGenreKey(genre);
        const genreData = GenreData[genreKey] || {};

        // Use the splitDescription function to split the description
        const { firstSentence, restOfDescription } = splitDescription(genreData.description || '');

        return {
          genre,
          percentage,
          color: shuffledColors[index % shuffledColors.length],
          ...genreData,
          description: restOfDescription, // restOfDescription now holds the truncated description without the first sentence
          firstSentence, // Add the first sentence to the object
        };
      }).filter(result => result && result.percentage > 0);

      parsed = parsed.sort((a, b) => b.percentage - a.percentage);

      setDetailedResults(parsed);
      setAnimate(true);
    }
  }, [results]);


  return (
    <div className={`results-display ${animate ? 'animate' : ''}`}>
    {fileName && <h2>{`Analysis results for: ${fileName}`}</h2>}

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
                {result.image && <img src={result.image} alt={`${result.genre}`} className="genre-image" />}
              </div>
              {/* Description container */}
              <div className="genre-description-container">
                <h3 className="genre-title">{result.genre.toUpperCase()}</h3>

                {/* Display the first sentence separately */}
                {result.firstSentence && (
                    <p className="genre-first-sentence">{result.firstSentence}</p>
                )}

                {/* Display the rest of the description */}
                <p className="genre-description">{result.description}</p>

                {result.readMoreLink && (
                    <a className="genre-read-more" href={result.readMoreLink} target="_blank" rel="noopener noreferrer">
                      Read more at music.ishkur.com...
                    </a>
                )}
              </div>
              {/* Artist list container */}
              <div className="genre-artists-container">
                <h4>RELATED ARTISTS:</h4>
                <ul className="artist-list">
                  {result.artists && result.artists.map((artist, artistIndex) => (
                      <li key={artistIndex} className="artist-name">
                        <a href={createWikiLink(artist)} target="_blank" rel="noopener noreferrer">
                          {artist}
                          </a>
                        </li>
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

