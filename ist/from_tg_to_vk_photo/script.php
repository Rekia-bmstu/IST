<?php

$access_token = "1e6fc5ae345b2af29028971a82627158b07cff065db6d25f57ed113ebf333135469fb4ff8004dc6a50da0";
$group_id = "АЙДИ_ГРУППЫ";
$album_id = 'АЙДИ ФОТОАЛЬБОМА';
$image_path = dirname(__FILE__) . '/Photo.jpg';

$vk = new Model_Vk($access_token);

//Загружаем изображение
$upload_img = $vk->uploadImage($image_path, null, null);

class Model_Vk {

    private $access_token;
    private $url = "https://api.vk.com/method/";

    /**
     * Конструктор
     */
    public function __construct($access_token) {

        $this->access_token = $access_token;
    }

    /**
     * Делает запрос к Api VK
     * @param $method
     * @param $params
     */
    public function method($method, $params = null) {

        $p = "";
        if( $params && is_array($params) ) {
            foreach($params as $key => $param) {
                $p .= ($p == "" ? "" : "&") . $key . "=" . urlencode($param);
            }
        }
        $response = file_get_contents($this->url . $method . "?" . ($p ? $p . "&" : "") . "access_token=" . $this->access_token);
        
        if( $response ) {
            return json_decode($response);
        }
        return false;
    }

  public function uploadImage($file, $group_id = null, $album_id = null) {

    $params = array();
    if( $group_id ) {
      $params['group_id'] = $group_id;
    }
    if( $album_id ) {
      $params['album_id'] = $album_id;
    }

    //Получаем сервер для загрузки изображения
    $response = $this->method("photos.getUploadServer", $params);


    if( isset($response) == false ) {
      print_r($response);
      exit;
    }
    
    $server = $response->response->upload_url;

    $postparam=array("file1"=>"@".$file);
    var_dump($postparam);
    //Отправляем файл на сервер
    var_dump($server);
    $ch = curl_init($server);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS,$postparam);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: multipart/form-data; charset=UTF-8'));
    $res = curl_exec($ch);
    var_dump($res);
    $json = json_decode($res);
    var_dump($json);
    curl_close($ch);


    

    
    //Сохраняем файл в альбом
    $photo = $this->method("photos.save", array(
      "server" => $json->server,
      "photos_list" => $json->photos_list,
      "album_id" => $album_id,
      "hash" => $json->hash,
      'gid' => $group_id
    ));
    
    print("WORKING");
    if( isset($photo->response[0]->id) ) {
      return $photo->response[0]->id;
    } else {
      return false;
    }
  }
}
?>