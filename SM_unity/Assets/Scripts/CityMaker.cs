using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// city maker script modified for the traffic simulation by Santiago Benitez and Sergio Zucckermann

public class CityMaker : MonoBehaviour
{
    [SerializeField] TextAsset layout;
    [SerializeField] GameObject roadPrefab;
    [SerializeField] GameObject emptyRoadPrefab;
    [SerializeField] GameObject buildingPrefab;
    [SerializeField] GameObject DestinationPrefab;
    [SerializeField] int tileSize;

    // Start is called before the first frame update
    void Start()
    {
        MakeTiles(layout.text);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void MakeTiles(string tiles)
    {
        int x = 0;
        // Mesa has y 0 at the bottom
        // To draw from the top, find the rows of the file
        // and move down
        // Remove the last enter, and one more to start at 0
        int y = tiles.Split('\n').Length - 2;
        Debug.Log(y);

        Vector3 position;
        GameObject tile;

        for (int i=0; i<tiles.Length; i++) {
            if (tiles[i] == '>' || tiles[i] == '<' || tiles[i] == 'v' || tiles[i] == '^') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                if (tiles[i] == '<'){
                    tile = Instantiate(roadPrefab, position, Quaternion.identity);
                    tile.transform.parent = transform;
                }
                else if (tiles[i] == '>'){
                    tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 180, 0));
                    tile.transform.parent = transform;
                }
                else if (tiles[i] == 'v'){
                    tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 270, 0));
                    tile.transform.parent = transform;
                }                
                else if (tiles[i] == '^'){
                    tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 90, 0));
                    tile.transform.parent = transform;
                }
                x += 1;

            } else if (tiles[i] == 's') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(emptyRoadPrefab, position, Quaternion.identity);
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'S') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(emptyRoadPrefab, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'D'){
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(DestinationPrefab, position, Quaternion.identity);
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == '#') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(buildingPrefab, position, Quaternion.identity);
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == '\n') {
                x = 0;
                y -= 1;
            }
        }

    }
}
