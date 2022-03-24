package org.powertac.samplebroker.services;

import java.util.ArrayList;

import com.google.gson.Gson;

import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.powertac.samplebroker.domain.PartialCleared;
import org.powertac.samplebroker.domain.PredictionKey;
import org.powertac.samplebroker.domain.PredictionResponse;
import org.powertac.samplebroker.repos.ClearedFuturesRepo;
import org.powertac.samplebroker.repos.ClearedRepo;
import org.powertac.samplebroker.repos.WeatherForecastRepo;
import org.powertac.samplebroker.repos.WeatherReportRepo;
import org.springframework.stereotype.Service;

@Service
public class API {

    private WeatherForecastRepo weatherForecastRepo = new WeatherForecastRepo();

    private WeatherReportRepo weatherReportRepo = new WeatherReportRepo();

    private ClearedRepo clearedRepo = new ClearedRepo();

    private ClearedFuturesRepo clearedFuturesRepo = new ClearedFuturesRepo();

    private Gson gson = new Gson();

    private PredictionResponse getPrediction(Integer timeslot, String url) {
        String data = buildPredictionData(timeslot-1);
//        System.out.println("Argument: " + data);
        CloseableHttpClient httpClient = HttpClients.createDefault();
        HttpPost httpPost = new HttpPost(url);
        httpPost.setHeader("Content-type", "application/json");
        try {
        	StringEntity stringEntity = new StringEntity(data);
            httpPost.setEntity(stringEntity);
            CloseableHttpResponse response = httpClient.execute(httpPost);
            String prediction = new BasicResponseHandler().handleResponse(response);
            PredictionResponse predictionResponse = gson.fromJson(prediction, PredictionResponse.class);
            return predictionResponse;
        } catch (Exception e) {
            return new PredictionResponse();
        }
    }

    /**
     * 
     * @param i Timeslot
     * @return
     */
    private String buildPredictionData(Integer i) {
        StringBuilder sb = new StringBuilder();
        sb.append("{\"data\":[[");
        sb.append(i % 24 + ",");	//Timeslot	Modulodivision -> 360 % 24 => 0 (end bootstrap 15 days), 385 % 24 => 1 (game start)
        sb.append(i % 168 + ","); 	//Weekday
        
        // CIRE feature set
        for (int j = 0; j < 24; j++) {
            sb.append(clearedFuturesRepo.findById(i + j).getQuantity().toString() + ",");	// CA_H-1
            sb.append(clearedFuturesRepo.findById(i + j).getMeanPrice().toString() + ",");	// CP_H-1
        }
        for (int j = 0; j < 24; j++) {
            sb.append(clearedFuturesRepo.findById(i + j - 24).getQuantity().toString() + ",");	// CA_D-1
            sb.append(clearedFuturesRepo.findById(i + j - 24).getMeanPrice().toString() + ",");	// CP_D-1
        }
        for (int j = 0; j < 24; j++) {
            sb.append(clearedFuturesRepo.findById(i + j - 168).getQuantity().toString() + ",");		// CA_W-1
            if (j < 23) {
            	sb.append(clearedFuturesRepo.findById(i + j - 168).getMeanPrice().toString() + ",");	// CP_W-1
            } else {
            	sb.append(clearedFuturesRepo.findById(i + j - 168).getMeanPrice().toString());			// CP_W-1
            }
            
        }
        
    	// TNE feature set
//        for (int j = 24; j > 0; j--) {
//            sb.append(clearedFuturesRepo.findById(i - j).getQuantity().toString() + ",");	// CA	Cleared Amount for timeslot i - j
//            sb.append(clearedFuturesRepo.findById(i - j).getMeanPrice().toString() + ",");	// CP	Cleared Price for timeslot i - j
//            sb.append(weatherReportRepo.findById(i - j).getTemperature() + ",");			// T	Temperature for timeslot i - j
//            sb.append(weatherReportRepo.findById(i - j).getWindSpeed() + ",");				// WS	Windspeed for timeslot i - j
//        }
//        sb.append(weatherReportRepo.findById(i).getTemperature() + ",");					// CT	Current Temperature
//        sb.append(weatherReportRepo.findById(i).getWindSpeed() + ",");        				// CWS	Current Windspeed
//        ArrayList<PartialCleared> partialCleared = clearedRepo.findById(i-1).getFutureCleared(); 
//        for (int k = 0; k < 24; k++) {
//            sb.append(partialCleared.get(k).getQuantity() + ",");							// PCA - Partial Cleared Amount
//            sb.append(partialCleared.get(k).getMeanPrice() + ",");							// PCP - Partial Cleared Price
//        }
//
//        for (int j = 1; j <= 24; j++) {
//            sb.append(weatherForecastRepo.findById(new PredictionKey(i, i + j)).getTemperature() + ",");	// TF	Temperature forecast
//            if (j < 24) {
//                sb.append(weatherForecastRepo.findById(new PredictionKey(i, i + j)).getWindSpeed() + ",");	// WSF	Windspeed forecast
//            } else {
//                sb.append(weatherForecastRepo.findById(new PredictionKey(i, i + j)).getWindSpeed());
//            }
//        }
        
        sb.append("]]}");
        return sb.toString();
    }

	public ArrayList<Double> predictAmounts(int currentTimeslot) {
        return getPrediction(currentTimeslot, "http://localhost:5000/predict/energy").getArray();
	}

	public ArrayList<Double> predictPrices(int currentTimeslot) {
        return getPrediction(currentTimeslot, "http://localhost:5000/predict/price").getArray();
	}
}