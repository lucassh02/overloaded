
function ListGroup() {
  let items = [
    "An item",
    "A second item",
    "A third item",
    "A fourth item",
    "And a fifth one",
  ];

  

  
    return (
    <>
        <h2>List Group</h2>
        {items.length === 0 && <p>No items to display</p>}
        <ul className="list-group">
            {items.map(item => <li className="list-group-item" key={item}>{item}</li>)}
        </ul>
    </>
  );
}

export default ListGroup;
