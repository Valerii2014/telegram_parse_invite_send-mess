const fs = require('fs')

const reverser = async (pathFrom, pathTo) => {
    const json = await fs.readFile(pathFrom, (err, data) => {
        if (err) console.log(err)
        else {
            const array = JSON.parse(data)
            const reverseArray = array.reverse()
            fs.writeFile(pathTo, JSON.stringify(reverseArray), (err) => {
                if (err) console.log(err)
                else {
                    console.log('File written successfully\n')
                }
            })
        }
    })
}

reverser(
    'jsonDB/sparsedChannelsUsers/uninvited_users.json',
    'jsonDB/sparsedChannelsUsers/uninvited_users_reverse.json'
)
