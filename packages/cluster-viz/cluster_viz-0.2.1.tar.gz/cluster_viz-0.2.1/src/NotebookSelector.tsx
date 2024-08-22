// NotebookSelector.tsx
import React, { useState, useEffect } from 'react';
import '../style/notebookSelector.css';

interface NotebookSelectorProps {
  notebookIds: number[];
  onSelectionChange: (selectedIds: number[]) => void;
}

const NotebookSelector: React.FC<NotebookSelectorProps> = ({ notebookIds, onSelectionChange }) => {
  const [shownNotebooks, setShownNotebooks] = useState<Set<number>>(new Set());
  const [selectedValue, setSelectedValue] = useState<string>('');

  useEffect(() => {
    // Trigger the callback when shownNotebooks changes
    onSelectionChange(Array.from(shownNotebooks));
  }, [shownNotebooks, onSelectionChange]);
  
  const handleRemoveNotebook = (notebookId: number) => {
    const newShownNotebooks = new Set(shownNotebooks);
    if(newShownNotebooks.has(notebookId)){
      newShownNotebooks.delete(notebookId);
      setShownNotebooks(newShownNotebooks);
    }
  };     

  const handleAddNotebook = () => {
    const notebookId = selectedValue === "ALL" ? -2 : Number(selectedValue);

    if (notebookId === -2) {
      // Remove all selected notebooks before adding ALL
      const newShownNotebooks = new Set<number>();
      newShownNotebooks.add(-2);
      setShownNotebooks(newShownNotebooks);
    } else if (!shownNotebooks.has(notebookId) && notebookIds.includes(notebookId)) {
      if (shownNotebooks.has(-2)) {
        console.log("nxdjwkn");
        handleRemoveNotebook(-2);  // Remove ALL (-2) before adding a specific notebook
        console.log("COME ON")
      }   
      console.log("notebooks")
      console.log(shownNotebooks)
      const newShownNotebooks = new Set(shownNotebooks);
      newShownNotebooks.add(notebookId);
      setShownNotebooks(newShownNotebooks);
    }
    setSelectedValue(''); // Clear the input after adding
  };   
   
  return ( 
    <div className="selector-container">
      <div className="current-selection-text">Current selection:</div>
      <div className="selected-elements" id="selected-elements">
        {Array.from(shownNotebooks).map(notebookId => (
          <div key={notebookId} className="element">
            {notebookId === -2 ? "ALL" : notebookId}
            <button className="remove-button" onClick={() => handleRemoveNotebook(notebookId)}>Remove</button>
          </div>
        ))}
      </div>
      <input
        type="text"
        list="elements"
        id="element-selector"
        className="element-selector"
        value={selectedValue}
        onChange={(e) => setSelectedValue(e.target.value)}
        placeholder="Select notebook ID"
      />
      <datalist id="elements">
        {notebookIds.map(id => (
          <option key={id} value={id === -2 ? "ALL" : id}>
            {id === -2 ? "ALL" : id}
          </option>
        ))}
      </datalist>
      <button id="add-button" onClick={handleAddNotebook}>
        +
      </button>
    </div>
  );
};

export default NotebookSelector;
